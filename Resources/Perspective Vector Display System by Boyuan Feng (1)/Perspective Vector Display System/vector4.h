#pragma once
#ifndef vector4_h

#define vector4_h

#include <iostream>
#include <cmath>

using namespace std;

class Vector4 {
public:

	double x, y, z, w;
	// Constructors
	Vector4() : x(0.0), y(0.0), z(0.0), w(1.0) {}
	Vector4(double _x, double _y, double _z) : x(_x), y(_y), z(_z), w(1.0) {}
	Vector4(double _x, double _y, double _z, double _w) : x(_x), y(_y), z(_z), w(_w) {}
};

#endif

