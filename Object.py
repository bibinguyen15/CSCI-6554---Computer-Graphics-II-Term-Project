import numpy as np
import random
from Project_2 import *


class Object:
    def __init__(self, file):
        fileName = "D files\\" + file + ".d.txt"
        self.polys, self.vertices = transformation(fileName)
        self.colors = self.getColors()
        self.yBounds = []

    # For constant shading, the colors are set to be random
    # The color list cotains a list of RGB values that corrensponds to the index of the polygon in polys
    def getColors(self):
        colors = []
        print("Number of polys:", len(self.polys))
        for poly in self.polys:
            colors.append(
                [random.random(), random.random(), random.random()])

        print(colors)


house = Object("house")
