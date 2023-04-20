from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np


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
            poly = [int(v) - 1 for v in data[n_ver + i].split()]
            polys.append(poly)

        print(polys)

    return vertices, polys


def unitVector(vector):
    mag = np.sqrt(np.sum([i**2 for i in vector]))
    return vector / mag


def drawFunc():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)

    # get vertices and polygons from file
    vertices, polys = read_file("house.d.txt")
    cam = np.array([0, 0, -20])

    pRef = np.array([0, 0, 0])

    # calculating U, V, N
    N = pRef - cam
    N = unitVector(N)

    print("N=", N)

    vPrime = np.array([0, 1, 0])

    U = np.cross(N, vPrime)
    U = unitVector(U)

    print("V prime=", vPrime, "and U=", U)

    V = np.cross(U, N)

    print("V=", V)

    T = np.array([[1, 0, 0, -cam[0]],
                  [0, 1, 0, -cam[1]],
                  [0, 0, 1, -cam[2]],
                  [0, 0, 0, 1]])
    print("T:\n", T)

    R = np.array([[U[0], V[0], N[0], 0],
                  [U[1], V[1], N[1], 0],
                  [U[2], V[2], N[2], 0],
                  [0, 0, 0, 1]])
    print("R:\n", R)

    mView = R.dot(T)
    print("M_view:\n", mView)

    d, f = 1, 100
    h = d / 2

    mPers = np.array([[d / h, 0, 0, 0],
                      [0, d / h, 0, 0],
                      [0, 0, f / (f - d), -d * f / (f - d)],
                      [0, 0, 1, 0]])
    print("M_pers:\n", mPers)

    # identity matrix: placing the object in the middle for simplicity
    mModel = np.array([[1, 0, 0, 0],
                       [0, 1, 0, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1]])
    print("M_model:\n", mModel)

    transform = mPers.dot(mView.dot(mModel))

    # print("Transformation:\n", transform[0][0])

    vertices = getVertices(vertices, transform)

    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    polys = [poly[1:] for poly in polys]
    for poly in polys:

        if True:
            glBegin(GL_POLYGON)
            for vertex in poly:
                print(vertex, end=" ")
                glVertex3f(vertices[vertex][0],
                           vertices[vertex][1], vertices[vertex][2])

            glEnd()
            print()

    glFlush()


def getVertices(vertices, transform):
    newVertices = []
    for vertex in vertices:
        vertex = vertex + [1]
        vertex = transform.dot(vertex)
        vertex = (vertex / vertex[-1])[:-1]
        newVertices.append(vertex)
    return newVertices


def main():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA)
    glutInitWindowPosition(0, 0)
    glutInitWindowSize(1000, 900)
    glutCreateWindow('Lab 1: Viewing Transformation')

    glutDisplayFunc(drawFunc)
    glutMainLoop()


if __name__ == '__main__':
    main()
