import librosa
import matplotlib.pyplot as plt
import librosa.display
import numpy as np
import sklearn
import IPython.display as ipd
from modules.tools import GetUniqueID
import os
from PIL import Image


def normalize(x, axis=0):
    return sklearn.preprocessing.minmax_scale(x, axis=axis)


class AudioFile:
    def __init__(self, path, transparent=False, color='#ffffff', edgecolor='#2d2d2d'):
        self.transparent = transparent
        self.color = color
        self.edgecolor = edgecolor
        self.path = path
        self.x, self.sr = librosa.load(path)
        self.spectral_centroids = librosa.feature.spectral_centroid(self.x, sr=self.sr)[
            0]
        self.stft = librosa.stft(self.x)
        self.m = librosa.feature.mfcc(self.x, sr=10)
        self.spectral_rolloff_ = librosa.feature.spectral_rolloff(
            self.x + 0.01, sr=self.sr)[0]
        # self.spec_bw = librosa.feature.spectral_bandwidth(y=self.x, sr=self.sr)
        # self.stft = librosa.stft(self.x)
        # self.S, self.phase = librosa.magphase(self.stft)
        # self.amp_to_db = librosa.amplitude_to_db(self.S, ref=np.max)

    def waveplot(self, audio_file, path):
        x, sr = self.x, self.sr
        l = plt.figure(figsize=(15, 5))
        librosa.display.waveplot(x, sr=sr)
        plt.savefig(os.path.join("static", "graphs",
                                 f"{path}.png"), transparent=self.transparent, facecolor=self.color)
        plt.clf()
        return l

    def spectrogram_linear(self, audio_file, path):
        x, sr = self.x, self.sr
        ft = self.stft
        db = librosa.amplitude_to_db(abs(ft))
        fig = plt.figure(figsize=(15, 5))
        librosa.display.specshow(db, sr=sr, x_axis='time', y_axis='hz')
        plt.colorbar()
        plt.savefig(os.path.join("static", "graphs", f"{path}.png"), transparent=self.transparent,
                    facecolor=self.color, edgecolor=self.edgecolor)
        plt.clf()
        return fig

    def give_frames(self, audio_file, path):
        spectral_centroids = self.spectral_centroids
        x, sr = self.x, self.sr
        T = 5.0
        t = np.linspace(0, T, int(T * sr), endpoint=False)  # time variable
        ipd.Audio(x, rate=sr)
        fig = plt.figure(figsize=(15, 4))
        frame = range(len(spectral_centroids))
        t = librosa.frames_to_time(frame)
        librosa.display.waveplot(x, sr=sr, alpha=0.4)
        plt.plot(t, normalize(spectral_centroids), color='b')
        plt.savefig(os.path.join("static", "graphs",
                                 f"{path}.png"), transparent=self.transparent, facecolor=self.color)
        plt.clf()
        return fig

    def spectral_rolloff(self, audio_file, path):
        spectral_centroids = self.spectral_centroids
        x, sr = self.x, self.sr
        frames = range(len(spectral_centroids))
        t = librosa.frames_to_time(frames)
        spectral_rolloff = self.spectral_rolloff_
        fig = plt.figure(figsize=(15, 4))
        librosa.display.waveplot(x, sr=sr, alpha=0.4)
        plt.plot(t, normalize(spectral_rolloff), color='r')
        plt.savefig(os.path.join("static", "graphs",
                                 f"{path}.png"), transparent=self.transparent, facecolor=self.color)
        plt.clf()
        return fig

    # def spectral_bandwith(self, audio_file, path):
    #     x, sr = self.x, self.sr
    #     S, phase = self.S, self.phase
    #     spec_bw = self.spec_bw
    #     plt.figure()
    #     plt.subplot(2, 1, 1)
    #     plt.semilogy(spec_bw.T, label='Spectral bandwidth')
    #     plt.ylabel('Hz')
    #     plt.xticks([])
    #     plt.xlim([0, spec_bw.shape[-1]])
    #     plt.legend()
    #     plt.subplot(2, 1, 2)
    #     librosa.display.specshow(self.amp_to_db, y_axis='log', x_axis='time')
    #     plt.title('log Power spectrogram')
    #     plt.savefig("static/graphs/{}.png".format(path))
    #     plt.clf()

    def zero_crossings(self, audio_file, n, m):
        x, sr = self.x, self.sr
        zero_crossings = librosa.zero_crossings(x[n:m], pad=False)
        return sum(zero_crossings)

    def mfcc(self, audio_file, path):
        x, sr = self.x, self.sr
        fs = 10
        m = self.m
        fig = plt.figure(figsize=(15, 7))
        librosa.display.specshow(m, sr=sr, x_axis='time')
        plt.savefig(os.path.join("static", "graphs",
                                 f"{path}.png"), transparent=self.transparent, facecolor=self.color)
        plt.clf()
        return fig

    def text_based(self, audio_file, path=''):
        x, sr = self.x, self.sr
        tempo, beat_frames = librosa.beat.beat_track(y=x, sr=sr)
        zero_crossings = sum(librosa.feature.zero_crossing_rate(x))
        return {"Tempo": tempo, "Beat frames": beat_frames, "Zero crossing rate": zero_crossings}


FUNCTIONS = {'waveplot': "Waveplot", 'spectrogram_linear': "Linear Spectrogram",
             'give_frames': "Frames", 'spectral_rolloff': "Spectral Rolloff", 'mfcc': "MFCC (Mel-Frequency Cepstral Coefficients)"}


def create_figures(audio_file, color="#ffffff", transparent=False, edgecolor='#000000'):
    Audio = AudioFile(audio_file, transparent=transparent,
                      color=color, edgecolor=edgecolor)
    filenames = {}
    for func in FUNCTIONS.keys():
        unique_filename = GetUniqueID("graphs", ".png")
        f = getattr(Audio, func)
        f(audio_file, path=unique_filename)
        filenames.update(
            {func: '{}.png'.format(unique_filename)})
    return filenames
