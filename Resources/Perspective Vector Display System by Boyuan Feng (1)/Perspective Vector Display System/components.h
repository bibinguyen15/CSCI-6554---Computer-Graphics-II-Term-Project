#pragma once

#include <vector>
#include "vector3.h"
#include "matrix4d.h"

class Poly {
public:
	int num_vertex;
	vector<int> idx_vertex;
};

typedef Vector3 Point;

class Object {
public:
	int num_points, num_polygons;
	vector<Point> points;
	vector<Poly> polygons;
};

class Camera {
public:
	Vector3 P_ref, C;
};

class World {
public:
	Vector3 X, Y, Z;
};