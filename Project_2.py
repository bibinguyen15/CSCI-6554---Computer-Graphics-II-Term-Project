from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
from Classes import *
from constants import *


# Different camera views
# cam = np.array([0, 0, -20])  # cow
#cam = np.array([-20, 0, -20])
cam = np.array([25, 35, -20])
# cam = np.array([30, -15, -30])  # house


# Shuttle camera angles
#cam = np.array([30, -15, 150])
#cam = np.array([30, 50, 150])
# cam = np.array([0, 0, 200])


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
    mag = np.sqrt(np.sum([i**2 for i in vector]))
    return vector / mag


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
def transformation(file):

    # get vertices and polygons from file
    vertices, polys = read_file(file)

    # Defining pRef, varies depending on objects
    # pRef = np.array([-10, 0, 0])
    # pRef = np.array([10, 15, 20])  # house from top
    pRef = np.array([10, 0, 20])  # house
    # pRef = np.array([0, 0, 0])  # cow

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

    # Back face culling to minimize
    newPolys = []
    for poly in polys:
        # calculating normal for backface culling
        v1 = vertices[poly[1]] - vertices[poly[0]]
        v2 = vertices[poly[2]] - vertices[poly[1]]
        normal = np.cross(v1, v2)

        # only proceed to add to list of polygons if not back-facing
        if normal[2] <= 0:
            newPolys.append(poly)

    # print(vertices)
    return newPolys, vertices


def drawFunc():
    '''
    Z buffer algorithm is also implemented here
    '''
    # openGL things
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)

    # initialize each objects
    camaro = Object("camaro")
    house = Object("house")
    cow = Object("cow")
    #bench = Object("bench")

    # initialize the image buffer and depth buffer
    image = np.zeros((1000, 1000, 3))
    depth = np.ones((1000, 1000))

    # Calling scan conversion for each object
    #house.scanConversion(image, depth)
    cow.scanConversion(image, depth)
    #bench.scanConversion(image, depth)
    camaro.scanConversion(image, depth)

    # Drawing the objects
    glBegin(GL_POINTS)
    for i in range(1000):
        for j in range(1000):
            if depth[i][j] != 1:
                glColor3f(image[i][j][0], image[i][j][1], image[i][j][2])
                glVertex2f(changeBack(i), changeBack(j))
    glEnd()
    glFinish()
    glFlush()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA)
    glutInitWindowPosition(0, 0)
    glutInitWindowSize(1000, 1000)
    glutCreateWindow('Lab 2: Scan Conversion and Z Buffer')

    glutDisplayFunc(drawFunc)
    glutMainLoop()


if __name__ == '__main__':
    main()