import cv2
import PIL
import numpy as np


class Background:
    def __init__(self, **kwargs):
        self.original_image = cv2.resize(
            kwargs["image"], (kwargs["width"], kwargs["height"]))
        original_bpm = int(kwargs["bpm"])
        self.bpm = original_bpm//2 if original_bpm > 100 else original_bpm
        self.beat_every_x_sec = kwargs["bpm"]/60
        self.dims = (int(kwargs["height"]), int(kwargs["width"]))
        self.blur_strenght = 0
        self.max_blur_effect_strenght = int(kwargs["max_blur_effect_strenght"])
        self.first_time = float(kwargs["first_time"])

    def get_frame(self, **kwargs):
        t = kwargs["time"]-self.first_time
        if abs(t % self.beat_every_x_sec) < 0.1:
            self.blur_strenght = self.max_blur_effect_strenght
        elif self.blur_strenght > 0:
            self.blur_strenght -= 1
        if self.blur_strenght > 0:
            return cv2.blur(self.original_image, (self.blur_strenght*2, self.blur_strenght*2))
        else:
            return self.original_image.copy()
