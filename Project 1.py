import OpenGL
import OpenGL.GL
import OpenGL.GLUT
import numpy


def read_file(file):
    with open(file, 'r') as f:
        # split each line into a data index
        data = f.readline()

        # number  of vertices and number of polygons
        n_ver, n_poly = int(data.split()[1]), int(data.split()[2])

        data = f.readlines()
        vertices, poly = [], []

        # processing the vertices
        vertices = []
        for i in range(n_ver):
            vertex = [float(p) for p in data[i].split()]
            vertices.append(vertex)

        print(vertices)

        polys = []
        # processing the polygons
        for i in range(n_poly):
            poly = [int(v) for v in data[n_ver + i].split()]
            polys.append(poly)

        print(polys)

    return vertices, polys


read_file("house.d.txt")
