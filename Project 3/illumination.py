import numpy as np
import random
from transformation import *


class Illumination:
    def __init__(self, ka, kd, ks, L, V, sourceLight):
        self.ka = ka
        self.kd = kd
        self.ks = ks
        self.sourceLight = sourceLight
        self.iAmbient = np.array([0.4, 0.4, 0.4])

        self.L = unitVector(L)
        self.V = unitVector(V)
        #self.L = L
        #self.V = V
        self.h = L + V
        self.h = unitVector(self.h)

    def phongIllumination(self, normal, n):
        #print(normal)

        ambient, diffuse, specular = np.zeros(3), np.zeros(3), np.zeros(3)
        intensity = np.zeros(3)

        ambient = self.ka * self.iAmbient
        diff = max(np.dot(normal, self.L), 0)
        diffuse = self.kd * self.sourceLight * diff

        R = 2 * normal * (np.dot(normal, self.L)) - self.L

        R = unitVector(R)
        #spec = max(np.dot(normal, R), 0)
        spec = max(np.dot(normal, self.h), 0)
        specular = self.ks * self.sourceLight * (spec ** n)

        intensity = ambient + diffuse + specular

        '''
        for i in range(3):
            ambient[i] = self.ka * self.iAmbient[i]
            diffuse[i] = self.kd * self.sourceLight[i] * \
                max(np.dot(normal, self.L), 0)
            specular[i] = self.ks * self.sourceLight[i] * \
                (max(np.dot(normal, self.h), 0))**n
            #specular[i] = self.ks * self.sourceLight[i] * \
            #(np.dot(self.V, R) ** n)
            #print("specular:", self.sourceLight[i])
            intensity[i] = ambient[i] + diffuse[i] + specular[i]
            '''
        #print(normal, ambient, diffuse, specular, intensity)
        return intensity

