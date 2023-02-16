#pragma once
#ifndef vector3_h

#define vector3_h

#include <iostream>
#include <cmath>
#include "vector4.h"

using namespace std;

class Vector3 {
public:

	double x, y, z;
	// Constructors

	// Constructors
	Vector3() : x(0.0), y(0.0), z(0.0) {}
	Vector3(double _x, double _y, double _z) : x(_x), y(_y), z(_z) {}
	Vector3(Vector4 v4): x(v4.x / v4.w), y(v4.y / v4.w),z(v4.z / v4.w){}

	// Change the status of a vector
	void unit();
	static Vector3 unit(const Vector3& v) { Vector3 u = Vector3(v); u.unit(); return u; }


	// Magnitude
	double magnitude() const { return (sqrt(pow(x, 2) + pow(y, 2) + pow(z, 2))); }


	// Dot or scalar product
	double dot(const Vector3& v) const { return (x * v.x + y * v.y + z * v.z); }
	static double dot(const Vector3& v1, const Vector3& v2) { return v1.dot(v2); }

	// Distance between two vectors
	double distance(const Vector3& v) const { return sqrt(pow(x - v.x, 2) + pow(y - v.y, 2) + pow(z - v.z, 2)); }


	// Optimised arithmetic methods
	static Vector3 add(const Vector3& v1, const Vector3& v2);
	static Vector3 subtract(const Vector3& v1, const Vector3& v2);
	static Vector3 cross(const Vector3& v1, const Vector3& v2);
	static Vector3 invert(const Vector3& v1);
	static Vector3 multiply(const Vector3& v1, const double& num) { Vector3 result; result.x = v1.x * num; result.y = v1.y * num; result.z = v1.z * num; return result;}
	static Vector3 divide(const Vector3& v1, const double& num) {Vector3 result; result.x = v1.x / num; result.y = v1.y / num; result.z = v1.z / num; return result;}

	// Vector arithmetic, addition, subtraction and vector product
	Vector3 operator-() const { return invert(*this); }
	Vector3 operator+(const Vector3& v) const { Vector3 tv; return add(*this, v); }
	Vector3 operator-(const Vector3& v) const { Vector3 tv; return subtract(*this, v); }
	Vector3 operator*(const Vector3& v) const { Vector3 tv; return cross(*this, v); }
	Vector3 operator*(const double& num) const { Vector3 tv; return multiply(*this, num); }
	Vector3 operator/(const double& num) const { Vector3 tv; return divide(*this, num); }

};

#endif

