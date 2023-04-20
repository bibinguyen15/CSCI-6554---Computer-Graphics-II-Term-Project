from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


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


def drawFunc():
    glClear(GL_COLOR_BUFFER_BIT)
    # glRotatef(0.1, 0.1, 0.5, 0)
    # glutWireTeapot(0.5)
    vertices, polys = read_file("house.d.txt")
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    vertices, polys = read_file("house.d.txt")
    polygon = [0, 4, 3, 2, 1]
    for vertex in polygon:
        glVertex3f(vertices[vertex][0],
                   vertices[vertex][1], vertices[vertex][2])
    glBegin(GL_LINES)

    glFlush()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA)
    glutInitWindowPosition(0, 0)
    glutInitWindowSize(400, 400)
    glutCreateWindow(b'first')
    glutDisplayFunc(drawFunc)
    glutMainLoop()


if __name__ == '__main__':
    main()
