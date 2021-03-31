from flask import Flask, render_template, url_for, redirect, request, flash, jsonify, session
from modules.graphs import create_figures
from modules.video import *
import os
from modules.tools import GetUniqueID
import json

app = Flask(__name__)
app.secret_key = '1234567890abcde'

widgetfile = open('data/about_the_widgets.json', 'r')
widgets = dict(json.load(widgetfile))


ALLOWED_EXTENSIONS = ['wav']


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/about-the-widget')
def about_the_widget():
    text = request.args.get('jsdata')
    about = widgets.get(str(text))
    print(about)
    return render_template('about-the-widget.html', about=about)


@app.route("/graph-audio-upload", methods=['GET'])
def graph_audio_upload():
    return render_template('graph-file-upload.html')


@app.route('/interactive-visualization', methods=['POST'])
def interactive():
    graphs = {}
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Please upload a file.')
            return redirect(request.url)
        file = request.files['file']
        if request.files['file'].filename == '':
            flash('No selected file')
            return redirect(request.url)
        if not allowed_file(file.filename):
            flash("Only {} extensions are allowed".format(
                ', '.join(ALLOWED_EXTENSIONS)))
            return redirect(request.url)

        filename = GetUniqueID("UPLOAD_AUDIO", "wav")
        file.save(os.path.join('static', 'UPLOAD_AUDIO', filename))
        audio_file = os.path.join('static', 'UPLOAD_AUDIO', filename)
        graphs = create_figures(audio_file)
    return render_template('graphs.html', graphs=graphs)


@ app.route('/visualize-with-video')
def video_form():
    return render_template("visualize.html")


@ app.route('/video-download', methods=['POST'])
def generate_video():
    src = ''
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Please upload a file.')
            return redirect(request.url)

        file = request.files['file']

        if request.files['file'].filename == '':
            flash('No selected file')
            return redirect(url_for("makevideo"))
        if not allowed_file(file.filename):
            flash("Only {} extensions are allowed".format(
                ', '.join(ALLOWED_EXTENSIONS)))
            return redirect(url_for("makevideo"))

        audio_filename = "{}.wav".format(GetUniqueID("UPLOAD_AUDIO", ".wav"))
        audio_file = os.path.join("static", 'UPLOAD_AUDIO', audio_filename)
        file.save(audio_file)
        parameters = {}
        default = {"widgetstring": "{widgets:[]}",
                   "fps": 30, "dims": "1280x720"}

        for prop in ["widgetstring", "fps", "dims"]:
            try:
                value = int(request.form.get(prop))
            except:
                try:
                    value = request.form.get(prop)
                except:
                    value = default[prop]
            parameters[prop] = value

        if request.files['background'].filename == '':
            background = None
        else:
            background = request.files.get("background")
        if not allowed_file(file.filename):
            flash(
                f"Only {', '.join(ALLOWED_EXTENSIONS)} extensions are allowed")
            return redirect(url_for("makevideo"))

        src = make_video(
            audio_file,
            parameters["widgetstring"],
            background,
            int(parameters["fps"]),
            int(parameters["dims"].split("x")[0]),
            int(parameters["dims"].split("x")[1])
        )
        audiopath = "http://localhost:5000/static/UPLOAD_AUDIO/" + audio_filename
        videopath = "http://localhost:5000/static/GENERATED_VIDEOS/" + src

        response = jsonify(video=videopath, audio=audiopath)
        response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
        return render_template('visualize_results.html', src=src, audio_src=audio_filename)


if __name__ == "__main__":
    app.run()
