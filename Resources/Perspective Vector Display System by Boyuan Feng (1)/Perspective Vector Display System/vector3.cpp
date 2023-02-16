#include "vector3.h"
#define EPSILON 1e-8


// Make a unit vector
void Vector3::unit() {
	double mag = magnitude();
	if (mag < EPSILON) {
		x = 0.0;
		y = 0.0;
		z = 0.0;
	}
	else {
		x /= mag;
		y /= mag;
		z /= mag;
	}
}


Vector3 Vector3::invert(const Vector3& v1) {
	Vector3 result;
	result.x = -v1.x;
	result.y = -v1.y;
	result.z = -v1.z;
	return result;
}


Vector3 Vector3::add(const Vector3& v1, const Vector3& v2) {
	Vector3 result;
	result.x = v1.x + v2.x;
	result.y = v1.y + v2.y;
	result.z = v1.z + v2.z;
	return result;
}


Vector3 Vector3::subtract(const Vector3& v1, const Vector3& v2) {
	Vector3 result;
	result.x = v1.x - v2.x;
	result.y = v1.y - v2.y;
	result.z = v1.z - v2.z;
	return result;
}


Vector3 Vector3::cross(const Vector3& v1, const Vector3& v2) {
	Vector3 result;
	result.x = v1.y * v2.z - v1.z * v2.y;
	result.y = v1.z * v2.x - v1.x * v2.z;
	result.z = v1.x * v2.y - v1.y * v2.x;
	return result;
}
