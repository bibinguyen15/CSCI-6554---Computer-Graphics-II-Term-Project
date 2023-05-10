import numpy as np
import random
from transformation import *
from texture import *

class Illumination:
    def __init__(self, ka, kd, ks, L, V, sourceLight):
        self.ka = ka
        self.kd = kd
        self.ks = ks
        self.sourceLight = sourceLight
        self.iAmbient = np.array([0.4, 0.4, 0.4])

        self.L = unitVector(L)
        self.V = unitVector(V)
        # self.L = L
        # self.V = V
        self.h = L + V
        self.h = unitVector(self.h)

    def phongIllumination(self, im, normal, n):
        # print(normal)
        texture = textureMapping(im.shape[0], im.shape[1], normal)
        # texture = textureMap(im.shape[0], im.shape[1], normal)
        u = texture[0] - 1
        v = texture[1] - 1

        ambient = self.ka * self.iAmbient
        diff = max(np.dot(normal, self.L), 0)
        diffuse = self.kd * self.sourceLight * diff

        R = 2 * normal * (np.dot(normal, self.L)) - self.L

        R = unitVector(R)
        spec = max(np.dot(normal, R), 0)
        # spec = max(np.dot(normal, self.h), 0)
        specular = self.ks * self.sourceLight * (spec ** n)

        intensity = (ambient + diffuse + specular) * im[int(u)][int(v)]/255
        # intensity = ambient + diffuse + specular
        # print(normal, ambient, diffuse, specular, intensity)
        return intensity
