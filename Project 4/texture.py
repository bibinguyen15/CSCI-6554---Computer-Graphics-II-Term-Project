# Texture file
from PIL import Image
import numpy as np
import math


def loadTexture(filename):
    im = np.array(Image.open(filename))

    height = im.shape[0]
    width = im.shape[1]
    print(width, height, im[1000][20])
    print(len(im))
    return im


def textureMapping(w, h, n):
    """
    Texture mapping using sphere mapping
    width, height, normal of pixel
    return: index of mapping position
    """

    theta = math.acos(n[0]) * 100 / math.pi
    u = (theta / 180) * w
    v = (n[1] + 1) * h / 2
    # print(u, v)
    return [u, v]


def textureMap(width, height, point):
    z = np.array([0, 0, 1])
    x = np.array([1, 0, 0])
    normal = point
    phi = math.acos(np.dot(z, normal) / (np.linalg.norm(z) * np.linalg.norm(normal)))

    n = np.array([normal[0], normal[1], 0])
    theta = math.acos(np.dot(x, n) / (np.linalg.norm(x) * np.linalg.norm(n)))

    u = theta / (math.pi / 2)
    v = (math.pi / 2 - phi) / (math.pi / 4)
    # print(f"phi = {phi}, theta = {theta}, pi = {math.pi}")
    print(u, v)

    return [u * width, v * height / 2]

