from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
from objects import *
from constants import *
from transformation import *


def main():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA)
    glutInitWindowPosition(0, 0)
    glutInitWindowSize(1000, 1000)
    glutCreateWindow('Lab 4: Texture Mapping')

    glutDisplayFunc(drawFunc)
    glutMainLoop()


def drawFunc():
    '''
    Z buffer algorithm is also implemented here
    '''
    # openGL things
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)

    illumination = Illumination(ka, kd, ks, L, V, sourceLight)

    # initialize each objects
    #house = Object('house', house_cam, house_pRef, illumination, mode=mode)
    # cow = Object("cow", cow_cam, cow_pRef, illumination, mode)
    # donut = Object('donut', cam, pRef, illumination, mode)
    betterBall = Object('better-ball', cam, pRef, illumination, mode)

    # initialize the image buffer and depth buffer
    image = np.zeros((1000, 1000, 3))
    depth = np.ones((1000, 1000))

    # Calling scan conversion for each object
    #house.color(image, depth)
    # cow.color(image, depth)
    # donut.color(image, depth)
    betterBall.color(image, depth)

    zbuffer = np.argwhere(depth != 1)

    # Drawing the objects
    glBegin(GL_POINTS)

    for pos in zbuffer:
        x, y = pos
        glColor3f(image[x][y][0], image[x][y][1], image[x][y][2])
        glVertex2f(changeBack(x), changeBack(y))

    glEnd()
    glFinish()
    glFlush()


if __name__ == '__main__':
    main()
