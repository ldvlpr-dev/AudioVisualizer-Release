import json
import numpy as np
from cv2 import VideoWriter, VideoWriter_fourcc
import cv2
import librosa
import os
from PIL import Image
from modules.background import Background
from modules.widgets import *
from modules.tools import GetUniqueID
import moviepy.editor as mp
from math import ceil


def make_video(audio_file, widgetstring, background=None, fps=24, width=1280, height=720):
    # sets the name of the destination file
    video_id = GetUniqueID("GENERATED_VIDEOS", ".mp4")
    filename = video_id + ".mp4"
    # loads the audio in time series and its sample rate
    time_series, sample_rate = librosa.load(audio_file)
    # gets the absolutae values of the stft operation
    stft = np.abs(librosa.stft(time_series, hop_length=512, n_fft=2048 * 4))
    # convert the amplitude based diagram into a db-based one
    spectrogram = librosa.amplitude_to_db(stft, ref=np.max)
    # gets the Discrete Fourier Transform sample frequencies
    frequencies = librosa.core.fft_frequencies(n_fft=2048 * 4)
    times = librosa.core.frames_to_time(np.arange(
        spectrogram.shape[1]), sr=sample_rate, hop_length=512, n_fft=2048 * 4)  # get each frame time's in seconds
    time_index_ratio = len(times) / times[len(times) - 1]
    frequencies_index_ratio = len(
        frequencies) / frequencies[len(frequencies) - 1]
    # estimates tempo
    bpm, beats = librosa.beat.beat_track(time_series, sample_rate)
    first_time = list(librosa.frames_to_time(beats, sr=sample_rate))[0]

    background = cv2.cvtColor(cv2.resize(np.array(Image.open(background) if background is not None else np.random.randint(
        255, 256, (width, height, 3), dtype=np.uint8), dtype=np.uint8), (width, height)), cv2.COLOR_RGB2BGR)
    backgroundEffect = False

    fourcc = VideoWriter_fourcc(*'avc1')
    video = VideoWriter(os.path.join(
        "static", "GENERATED_VIDEOS", filename), fourcc, float(fps), (width, height))

    base_freqs = frequencies
    analyzed_freqs = [frequencies[i]
                      for i in range(0, len(base_freqs), len(base_freqs)//26)]
    while len(analyzed_freqs) > 26:
        analyzed_freqs.pop()

    widgetsSrc = {
        "circularBeatVisualizer": BeatVisualizer,
        "circularBeatVisualizer_default": {
            "color": (0, 0, 0),
            "first_time": first_time,
            "bpm": bpm,
            "x": 0,
            "y": 0,
            "max_effect_strenght": 50,
            "min_height": 100,
            "thickness": 14,
            "decreasing_step": 1,
            "delay_tolerance": 0.1,
        },
        "freqVolumeBars": FreqVisualizerGroup,
        "freqVolumeBars_default": {
            "s_width": width,
            "s_height": height,
            "direction": "down",
            "freqvolumetype": "rectangle",
            "color": (0, 0, 0),
            "bpm": bpm,
            "freqs": analyzed_freqs,
            "x": 0,
            "y": 0,
            "circle_y_gap": 2,
            "max_effect_strenght": 50,
            "min_height": 10,
            "thickness": 10,
            "delay_tolerance": 0.1,
            "width": width//26,
            "max_height": 300,
            "min_decibel": -80,
            "max_decibel": 0,
        },
        "colorWoofer": ColorWoofer,
        "colorWoofer_default": {
            "color": (0, 0, 0),
            "bpm": bpm,
            "freqs": [freq for freq in frequencies][1:6],
            "x": 0,
            "y": 0,
            "thickness": 10,
            "width": 50,
            "height": 100,
            "min_decibel": 300,
            "max_decibel": 10000
        },
    }

    widgets = []
    query = json.loads(widgetstring)["widgets"]

    for widget in query:
        params = {}
        if widget["name"] == "blurryBackground":
            if backgroundEffect:
                continue
            backgroundEffect = True
            background = Background(**{
                "image": background,
                "height": height,
                "width": width,
                "bpm": bpm,
                "first_time": first_time,
                "max_blur_effect_strenght": 5,
            })
            continue
        elif not widget["name"].endswith("_default") and widget["name"] in widgetsSrc.keys():
            toHave = list(widgetsSrc[widget["name"]+"_default"].keys())
        else:
            break
        for param in toHave:
            try:
                params[param] = widget[param]
            except KeyError:
                params[param] = widgetsSrc[widget["name"]+"_default"][param]
        params["name"] = widget["name"]
        widgets.append(widgetsSrc[widget["name"]](**params))

    duration = librosa.get_duration(filename=audio_file)
    freqN = len(frequencies)-1
    timesN = len(times)-1

    def get_decibel(target_time, freq):
        return spectrogram[min(int(freq * frequencies_index_ratio), freqN)][min(int(target_time * time_index_ratio), timesN)]

    def get_ms(i):
        return (i/fps)*1000

    def get_s(i):
        return i/fps

    i = 0
    getTicksLastFrame = 0

    for i in range(ceil(duration*fps)):
        t = get_ms(i)
        ts = get_s(i)

        if backgroundEffect:
            frame = background.get_frame(time=ts)
        else:
            frame = background.copy()

        deltaTime = (t - getTicksLastFrame) / 1000.0
        getTicksLastFrame = t

        for widget in widgets:
            if widget.name == "circularBeatVisualizer":
                widget.draw(dt=deltaTime, time=ts, frame=frame)
            elif widget.name == "freqVolumeBars":
                widget.draw(dt=deltaTime, db=[get_decibel(
                    t/1000, freq) for freq in widget.freqs], frame=frame)
            elif widget.name == "colorWoofer":
                widget.draw(db=[get_decibel(ts, freq)
                                for freq in widget.freqs], frame=frame)
            elif widget.name == "text":
                widget.draw(frame)

        video.write(frame)

    video.release()
    filename2 = video_id + "_audio.mp4"
    videoClip = mp.VideoFileClip(os.path.join(
        "static", "GENERATED_VIDEOS", filename))
    audioClip = mp.AudioFileClip(audio_file)
    final = videoClip.set_audio(audioClip)
    final.write_videofile(os.path.join(
        "static", "GENERATED_VIDEOS", filename2), fps=fps, codec="libx264", audio_codec="libvorbis", bitrate="6000k")
    return filename2
