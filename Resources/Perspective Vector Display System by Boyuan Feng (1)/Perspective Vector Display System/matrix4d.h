#pragma once
#ifndef matrix4d_h

#define matrix4d_h


#include <iostream>
#include <cmath>
#include "vector4.h"


class Matrix4d

{
public:
	double values[4][4] = { {1, 0, 0, 0}, {0, 1, 0, 0}, {0, 0, 1, 0}, {0, 0, 0, 1 } };


	// Constructors
	Matrix4d();
	Matrix4d(double Phi, double Theta, double Psi);
	Matrix4d(double v00, double v01, double v02, double v03, double v10, double v11, double v12, double v13, double v20, double v21, double v22, double v23, double v30, double v31, double v32, double v33);


	// Selectors

	double operator()(int row, int column) const { return values[row][column]; }
	double& operator()(int row, int column) { return values[row][column]; }


	// Optimised artimetric methods
	static Matrix4d add(const Matrix4d& m1, const Matrix4d& m2);
	static Matrix4d subtract(const Matrix4d& m1, const Matrix4d& m2);
	static Matrix4d mm(const Matrix4d& m1, const Matrix4d& m2);
	static Matrix4d mn(const Matrix4d& m1, const double& scale);
	static Vector4 mv(const Matrix4d& m1, const Vector4& v);


	// Matrix arithmetic
	Matrix4d operator+(const Matrix4d& m) const { return add(*this, m); }
	Matrix4d operator-(const Matrix4d& m) const { return subtract(*this, m); }
	Matrix4d operator*(const Matrix4d& m) const { return mm(*this, m); }
	Matrix4d operator*(const double& num) const { return mn(*this, num); }
	Vector4 operator*(const Vector4& v) const { return mv(*this, v); }


	// Transpose
	Matrix4d transpose();
	static Matrix4d transpose(const Matrix4d& m, Matrix4d& result) { result = m; return result.transpose(); }
	static Matrix4d transpose(const Matrix4d& m) { return Matrix4d(m).transpose(); }


};

#endif
