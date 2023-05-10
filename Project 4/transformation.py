import numpy as np
from constants import *


# Function to read file into list of vertices and list of polygons
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

        polys = []
        # processing the polygons
        for i in range(n_poly):
            poly = [int(v) - 1 for v in data[n_ver + i].split()]
            polys.append(poly)

    return vertices, polys


# Function to return a unit vector of a vector
def unitVector(vector):
    if np.linalg.norm(vector):
        return vector / np.linalg.norm(vector)
    return vector

# Function that applies the transformation on each vertex


def getVertices(vertices, transform):
    newVertices = []
    for vertex in vertices:
        vertex = vertex + [1]  # make into 4D
        vertex = transform.dot(vertex)  # transformation matrix
        # Divide by z before return to 3D
        vertex = (vertex / vertex[-1])[:-1]
        newVertices.append(vertex)

    # print(newVertices)
    return newVertices


# Main drawing function
def transformation(file, cam, pRef):

    # get vertices and polygons from file
    vertices, polys = read_file(file)

    # calculating U, V, N
    N = pRef - cam
    N = unitVector(N)

    vPrime = np.array([0, 1, 0])

    U = np.cross(N, vPrime)
    U = unitVector(U)

    V = np.cross(U, N)

    # T and R arrays for translation and rotation
    T = np.array([[1, 0, 0, -cam[0]],
                  [0, 1, 0, -cam[1]],
                  [0, 0, 1, -cam[2]],
                  [0, 0, 0, 1]])

    R = np.array([[U[0], U[1], U[2], 0],
                  [V[0], V[1], V[2], 0],
                  [N[0], N[1], N[2], 0],
                  [0, 0, 0, 1]])

    # mView matrix is R dot T
    mView = R.dot(T)

    # defining d, f, h
    d, f = 1, 1000
    h = d / 2

    # mPers matrix
    mPers = np.array([[d / h, 0, 0, 0],
                      [0, d / h, 0, 0],
                      [0, 0, f / (f - d), -d * f / (f - d)],
                      [0, 0, 1, 0]])

    # identity matrix: placing the object in the middle for simplicity
    mModel = np.array([[1, 0, 0, 0],
                       [0, 1, 0, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1]])

    # the transform matrix will be applied to each vertex for transformation
    transform = mPers.dot(mView.dot(mModel))

    # call getVertices for transformed vertices
    vertices = getVertices(vertices, transform)

    # since glVertex3f does not need the number of verticesm we can simplify
    polys = [poly[1:] for poly in polys]

    polyNormals = []
    for poly in polys:
        # calculating normal for backface culling
        v1 = vertices[poly[1]] - vertices[poly[0]]
        v2 = vertices[poly[2]] - vertices[poly[1]]
        normal = np.cross(v1, v2)

        polyNormals.append(unitVector(normal))

    return polys, vertices, polyNormals


#Function to change the values back into float instead of by screensize
def changeBack(value, coordinate=0):
    # 0 if value is x or y
    if coordinate == 0:
        result = value / 1000 * 2 - 1
    else:
        result = value / 1000
    return result
