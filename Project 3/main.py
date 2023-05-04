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
    glutCreateWindow('Lab 3: Shading and Illumination Models')

    glutDisplayFunc(drawFunc)
    glutMainLoop()


def drawFunc():
    '''
    Z buffer algorithm is also implemented here
    '''
    # openGL things
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)

    illumination = Illumination(ka, kd, ks, L, V, sourceColor)
    #illumination.setLight()

    # initialize each objects
    #cow = Object("cow", cam, cow_pRef, illumination, mode)
    house = Object('house', house_cam, house_pRef, illumination, mode=mode)
    #betterBall = Object('better-ball', cam,
    #betterBall_pRef, illumination, mode=mode)

    # initialize the image buffer and depth buffer
    image = np.zeros((1000, 1000, 3))
    depth = np.ones((1000, 1000))

    # Calling scan conversion for each object
    #cow.color(image, depth)
    #betterBall.color(image, depth)
    house.color(image, depth)

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
