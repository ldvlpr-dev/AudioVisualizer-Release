import cv2
import numpy as np


def hex_to_bgr(hx):
    hx = hx.lstrip('#')
    return tuple(int(hx[i:i + 2], 16) for i in (0, 2, 4))[::-1]


class Rectangle:
    def __init__(self, x, y, width, height, max_height, min_db, max_db, color, thickness, reverse):
        self.rev = -1 if reverse else 1
        self.x = x
        self.y = y
        self.width = width
        self.x2 = self.x + self.width
        self.color = color
        self.thickness = thickness
        self.min_height = height
        self.max_height = max_height
        self.max_db = max_db
        self.min_db = min_db
        self.height = height
        self.ratio = (self.max_height - self.min_height)/(
            self.max_db - self.min_db)

    def draw(self, db, dt, frame):
        desired_height = db * self.ratio + self.max_height
        speed = (desired_height - self.height)/0.1
        self.height += speed * dt
        self.height = max(
            min(self.height, self.max_height), self.min_height)

        cv2.rectangle(
            frame,
            (int(self.x), int(self.y)),
            (int(self.x2), int(self.y+self.height)),
            color=self.color,
            thickness=self.thickness
        )


class Circle:
    def __init__(self, x, y, width, height, max_height, min_db, max_db, color, thickness):
        self.x = x
        self.y = y
        self.width = width
        self.color = color
        self.thickness = thickness
        self.min_height = height
        self.max_height = max_height
        self.max_db = max_db
        self.min_db = min_db
        self.height = height
        self.ratio = (self.max_height - self.min_height)/(
            self.max_db - self.min_db)

    def draw(self, db, dt, frame):
        desired_height = db * self.ratio + self.max_height
        speed = (desired_height - self.height)/0.1
        self.height += speed * dt
        self.height = max(
            min(self.height, self.max_height), self.min_height)

        cv2.circle(frame, center=(int(self.x), int(self.y)), radius=int(
            self.height), color=self.color, thickness=self.thickness, lineType=cv2.LINE_AA)


class ColorWoofer:
    def __init__(self, **kwargs):
        self.name = kwargs["name"]
        self.x, self.y, self.freqs = int(
            kwargs["x"]), int(kwargs["y"]), kwargs["freqs"]
        self.colors = [(255, 0, 0), (0, 0, 255)]
        self.thickness = int(kwargs["thickness"])
        self.height = int(kwargs["height"])
        self.min_decibel = int(kwargs["min_decibel"])
        self.max_decibel = int(kwargs["max_decibel"])
        self.colorsLen = len(self.colors)
        self.ratio = (self.max_decibel-self.min_decibel)/(len(self.colors)-1)

    def draw(self, db, frame):
        db = min(-sum(db), self.max_decibel)
        if db <= self.min_decibel:
            color = self.colors[0]
        else:
            color = self.colors[min(
                int(self.ratio*(self.max_decibel-db)), self.colorsLen-1)]
        cv2.circle(frame, center=(int(self.x), int(self.y)), radius=int(
            self.height), color=color, thickness=self.thickness, lineType=cv2.LINE_AA)


class FreqVisualizerGroup:
    def __init__(self, **kwargs):
        self.direction = kwargs['direction']
        self.type = kwargs["freqvolumetype"]
        self.name = kwargs["name"]
        self.freqs = kwargs["freqs"]
        self.x = 0
        self.y = int(kwargs["s_height"]) if self.direction == "up" else 0
        self.color = hex_to_bgr(kwargs["color"])
        self.thickness = int(kwargs["thickness"])
        self.width, self.min_height, self.max_height = int(kwargs[
            "width"]), int(kwargs["min_height"]), int(kwargs["max_height"])
        self.min_decibel = int(kwargs["min_decibel"])
        self.max_decibel = int(kwargs["max_decibel"])
        self.shapes = []
        if self.type == "rectangle":
            for i in range(len(self.freqs)):
                self.shapes.append(
                    Rectangle(self.x + i*self.width, self.y, self.width, self.min_height, self.max_height, self.min_decibel, self.max_decibel, self.color, self.thickness, True if self.direction == "up" else False))
        elif self.type == "circle":
            self.y = (self.y - int(kwargs["circle_y_gap"]) - self.max_height) if self.direction == "up" else (
                self.y + int(kwargs["circle_y_gap"]) + self.max_height)
            for i in range(len(self.freqs)):
                self.shapes.append(
                    Circle(self.x + i*self.width, self.y, self.width, self.min_height, self.max_height, self.min_decibel, self.max_decibel, self.color, self.thickness))

    def draw(self, dt, db, frame):
        for (i, shape) in enumerate(self.shapes):
            shape.draw(db[i], dt, frame)


class BeatVisualizer:
    def __init__(self, **kwargs):
        self.name = kwargs["name"]
        self.x, self.y, self.min_height, self.height, self.color = int(kwargs["x"]), int(kwargs[
            "y"]), int(kwargs["min_height"]), int(kwargs["min_height"]), hex_to_bgr(kwargs["color"])
        self.beat_every_x_sec = int(kwargs["bpm"])/60
        self.effect_strenght = 0
        self.max_effect_strenght = int(kwargs["max_effect_strenght"])
        self.delay_tolerance = kwargs["delay_tolerance"]
        self.thickness = int(kwargs["thickness"])
        self.first_time = float(kwargs["first_time"])
        self.speed = 200

    def draw(self, **kwargs):
        t = kwargs["time"]-self.first_time
        if t < 0:
            pass
        elif abs(t % self.beat_every_x_sec) < self.delay_tolerance:
            self.effect_strenght = self.max_effect_strenght
        if self.effect_strenght < 0:
            self.effect_strenght = 0
        self.effect_strenght -= kwargs["dt"] * self.speed
        cv2.circle(kwargs["frame"], center=(int(self.x), int(self.y)), radius=int(
            self.min_height + self.effect_strenght), color=self.color, thickness=self.thickness, lineType=cv2.LINE_AA)
