// standard, set to release x86
#include <algorithm>
#include <iomanip>
#include <fstream>
#include <iostream>
#include <assert.h>
#include <math.h>
#include <time.h>  
#include <string>
#include <vector>
#include <sstream>
#include <stdio.h>
#include <cstdlib>
#include <cmath>
#include "GL/glut.h"
#include "matrix4d.h"
#include "vector3.h"
#include "vector4.h"
#include "components.h"
#define M_PI 3.1415926
#define EPSILON 1e-8

using namespace std;

vector<Object> objects;
Camera c;   // the camera
World w;    // the world coordinate system
Matrix4d M_model, M_view, M_pers, M_tf; // matrix of model, view, perspective and tranformation
Vector3 velocity;   // velocity of the camera

void print(Matrix4d M) {
    cout << M.values[0][0] << ", " << M.values[0][1] << ", " << M.values[0][2] << ", " << M.values[0][3] << ", " << endl;
    cout << M.values[1][0] << ", " << M.values[1][1] << ", " << M.values[1][2] << ", " << M.values[1][3] << ", " << endl;
    cout << M.values[2][0] << ", " << M.values[2][1] << ", " << M.values[2][2] << ", " << M.values[2][3] << ", " << endl;
    cout << M.values[3][0] << ", " << M.values[3][1] << ", " << M.values[3][2] << ", " << M.values[3][3] << ", " << endl;
}

bool isBackFace(Vector3 p0, Vector3 p1, Vector3 p2, Matrix4d M_tf) {
    p0 = Vector3::unit(Vector3(M_tf * Vector4(p0.x, p0.y, p0.z)));
    p1 = Vector3::unit(Vector3(M_tf * Vector4(p1.x, p1.y, p1.z)));
    p2 = Vector3::unit(Vector3(M_tf * Vector4(p2.x, p2.y, p2.z)));
    return (((p1 - p0) * (p2 - p1)).z > 0);
}

void drawObject(Object ob, Matrix4d M_tf) {
    for (int i = 0; i < ob.num_polygons; i++) {
        if (ob.polygons[i].num_vertex > 2 && isBackFace(ob.points[ob.polygons[i].idx_vertex[0] - 1], ob.points[ob.polygons[i].idx_vertex[1] - 1], ob.points[ob.polygons[i].idx_vertex[2] - 1], M_tf)) {
            continue;
        }
        glBegin(GL_LINE_LOOP);
        glColor3f(0.5f, 0.4f, 0.4f); // brunette
        for (int j = 0; j < ob.polygons[i].num_vertex; j++) {
            Vector3 point = ob.points[ob.polygons[i].idx_vertex[j] - 1];
            point = Vector3(M_tf * Vector4 (point.x, point.y, point.z, 1.0));
            glVertex3f(point.x, point.y, point.z);
        }
        glEnd();
    }
}

void display() {
    glClearColor(250.0f / 255.0f, 230.0f / 255.0f, 230.0f / 255.0f, 1.0f); // Set background color to black and opaque
    glClearDepth(1.0);
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    // render state
    glEnable(GL_DEPTH_TEST);
    glShadeModel(GL_SMOOTH);
    for (int i = 0; i < objects.size(); i++) {
        drawObject(objects[i], M_tf);
    }
    glutSwapBuffers();
}

Object loadfile(string file_path, bool clockwise=true)
{
    ifstream infile;
    string buff;
    string str;
    Object ob;
    vector<int> nums;

    infile.open(file_path);
    if (!infile) {
        std::cout << "Failed to Open File" << endl;
    }
    getline(infile, buff);  // load the first line
    istringstream ss(buff); // convert to string stream
    while (ss >> str) {     // get input from string stream, stop when encounter a separator
        if (str[0] >= '0' && str[0] <= '9') {   // get numbers, omit "data"
            nums.push_back(stoi(str));          // string to int
        }
    }
    ob.num_points = nums[0];
    ob.num_polygons = nums[1];
    ob.polygons = vector<Poly>(nums[1]);
    vector<vector<float> >points = vector<vector<float> >(nums[0]);
    vector<vector<int> >polygons = vector<vector<int> >(nums[1]);
    int count = 0;
    while (getline(infile, buff)) {
        istringstream ss(buff);
        while (ss >> str) {
            if (count < nums[0]) {
                points[count].push_back(stod(str));    // string to doule
            }
            else {
                polygons[count - nums[0]].push_back(stoi(str));
            }
        }
        count++;
    }
    for (int i = 0; i < nums[0]; i++) {
        ob.points.push_back(Point(points[i][0], points[i][1], points[i][2]));
    }
    if (!clockwise) {   // if counter-clockwise, read the data sequentially
        for (int i = 0; i < nums[1]; i++) {
            ob.polygons[i].num_vertex = polygons[i][0];
            for (int j = 1; j < polygons[i].size(); j++) {
                ob.polygons[i].idx_vertex.push_back(polygons[i][j]);
            }
        }
    }
    else {
        for (int i = 0; i < nums[1]; i++) {
            ob.polygons[i].num_vertex = polygons[i][0];
            for (int j = polygons[i].size() - 1; j > 0; j--) {
                ob.polygons[i].idx_vertex.push_back(polygons[i][j]);
            }
        }
    }
    return ob;
}

// calculate M_View
Matrix4d getMatrixView(Camera c, World w) {
    Vector3 N = Vector3::unit(c.P_ref - c.C);
    Vector3 U = Vector3::unit(N * w.Y);
    Vector3 V = U * N;
    Matrix4d M_view = Matrix4d(U.x, U.y, U.z, 0, V.x, V.y, V.z, 0, N.x, N.y, N.z, 0, 0, 0, 0, 1) *
        Matrix4d(1, 0, 0, -c.C.x, 0, 1, 0, -c.C.y, 0, 0, 1, -c.C.z, 0, 0, 0, 1);
    return M_view;
}

// calculate M_pers
Matrix4d getMatrixPerspective(float fovy, float aspect, float zNear, float zFar) {
    float d = zNear, f=zFar;
    float scale = 1 / tan(fovy * 0.5 * M_PI / 180);
    Matrix4d M_pers(scale / aspect, 0, 0, 0, 0, scale, 0, 0, 0, 0, f / (f - d), - d * f / (f - d), 0, 0, 1, 0);
    return M_pers;
}


void updateMatrixModel(Matrix4d M) {
    M_model = M;
}

void updateMatrixView(Matrix4d M) {
    M_view = M;
}

void updateMatrixPerspective(Matrix4d M) {
    M_pers = M;
}

void updateMatrixTransform(Matrix4d M) {
    M_tf = M;
}

void updateMatrixTransform() {
    M_tf = M_pers * M_view * M_model;
}


void reshape(int w, int h) {
    // viewport
    updateMatrixPerspective(getMatrixPerspective(90, w / h, 1, 60));
    updateMatrixTransform();
    glutPostRedisplay();
}


void timer(int t) {
    // render
    glutPostRedisplay();
    // velocity of the camera for house
    /*if (fabs(c.C.x + 20) < EPSILON && fabs(c.C.y + 20) < EPSILON) {
        velocity = Vector3(0, 0.1, 0);
    }
    else if (fabs(c.C.x + 20) < EPSILON && fabs(c.C.y - 20) < EPSILON) {
        velocity = Vector3(0.1, 0, 0);
    }
    else if (fabs(c.C.x - 20) < EPSILON && fabs(c.C.y - 20) < EPSILON) {
        velocity = Vector3(0, -0.1, 0);
    }
    else if (fabs(c.C.x - 20) < EPSILON && fabs(c.C.y + 20) < EPSILON) {
        velocity = Vector3(-0.1, 0, 0);
    }*/
    // velocity of the camera for king and face
    if (fabs(c.C.y + 5) < EPSILON) {
        velocity = Vector3(0, 0.04, 0);
    }
    else if (fabs(c.C.y - 10) < EPSILON) {
        velocity = Vector3(0, -0.04, 0);
    }
    c.C = c.C + velocity;
    updateMatrixView(getMatrixView(c, w));
    updateMatrixTransform();
    // 16 ms per frame ( about 60 frames per second )
    glutTimerFunc(16, timer, t);
}

// Main function: GLUT runs as a console application starting at main()
int main(int argc, char** argv) {
    glutInit(&argc, argv);          // initialize GLUT
    glutInitWindowSize(500, 500);   // set the window's initial width & height
    glutInitWindowPosition(50, 50); // position the window's initial top-left corner
    glutCreateWindow("lab1");       // create a window with the given title

    //double x;
    //cin >> x;

    c.P_ref = Vector3(0, 0, 0);
    w.Y = Vector3(0, 1, 0);

    // for house
    /*objects.push_back(loadfile("house.d.txt", false));
    c.C = Vector3(-20, -20, 80);
    M_model.values[0][3] = -8;*/

    // for king
    objects.push_back(loadfile("king.d.txt", true));
    c.C = Vector3(0, -5, 10);
    
    // for face
    //objects.push_back(loadfile("face.d.txt", true));
    //c.C = Vector3(0, -5, 8);
    updateMatrixModel(Matrix4d(-90 * M_PI / 180, 0, 0));
    M_view = getMatrixView(c, w);
    M_pers = getMatrixPerspective(90, 1, 1, 60);
    updateMatrixTransform(M_pers * M_view * M_model);   // calculate matrix of transformation

    glutPostRedisplay();
    glutDisplayFunc(display); // register display callback handler for window re-paint
    glutReshapeFunc(reshape);
    glutTimerFunc(16, timer, 0);
    glutMainLoop();           // enter the event-processing loop
    return 0;
}