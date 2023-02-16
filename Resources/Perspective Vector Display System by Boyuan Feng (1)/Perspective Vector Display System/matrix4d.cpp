#include "matrix4d.h"
#include "vector4.h"
#define EPSILON 1e-8

Matrix4d::Matrix4d() {
	values[0][0] = 1.0;
	values[1][1] = 1.0;
	values[2][2] = 1.0;
	values[3][3] = 1.0;
}

Matrix4d::Matrix4d(double v00, double v01, double v02, double v03, double v10, double v11, double v12, double v13, double v20, double v21, double v22, double v23, double v30, double v31, double v32, double v33) {
	values[0][0] = v00;
	values[0][1] = v01;
	values[0][2] = v02;
	values[0][3] = v03;
	values[1][0] = v10;
	values[1][1] = v11;
	values[1][2] = v12;
	values[1][3] = v13;
	values[2][0] = v20;
	values[2][1] = v21;
	values[2][2] = v22;
	values[2][3] = v23;
	values[3][0] = v30;
	values[3][1] = v31;
	values[3][2] = v32;
	values[3][3] = v33;
}


Matrix4d::Matrix4d(double Phi, double Theta, double Psi) {

	double c1 = cos(Phi), s1 = sin(Phi), c2 = cos(Theta), s2 = sin(Theta), c3 = cos(Psi), s3 = sin(Psi);

	values[0][0] = c2 * c3;

	values[0][1] = -c2 * s3;

	values[0][2] = s2;

	values[1][0] = s1 * s2 * c3 + c1 * s3;

	values[1][1] = -s1 * s2 * s3 + c1 * c3;

	values[1][2] = -s1 * c2;

	values[2][0] = -c1 * s2 * c3 + s1 * s3;

	values[2][1] = c1 * s2 * s3 + s1 * c3;

	values[2][2] = c1 * c2;

}


Matrix4d Matrix4d::add(const Matrix4d& m1, const Matrix4d& m2) {
	Matrix4d result;
	for (int i = 0; i < 4; i++)
	{
		for (int j = 0; j < 4; j++)
		{
			result.values[i][j] = m1.values[i][j] + m2.values[i][j];
		}
	}
	return result;

}


Matrix4d Matrix4d::subtract(const Matrix4d& m1, const Matrix4d& m2) {
	Matrix4d result;
	for (int i = 0; i < 4; i++)
	{
		for (int j = 0; j < 4; j++)
		{
			result.values[i][j] = m1.values[i][j] - m2.values[i][j];
		}
	}
	return result;
}


Matrix4d Matrix4d::mm(const Matrix4d& m1, const Matrix4d& m2) {
	Matrix4d result;
	for (int i = 0; i < 4; i++)
	{
		for (int j = 0; j < 4; j++)
		{
			double v = 0;
			for (int k = 0; k < 4; k++)
			{
				v += m1.values[i][k] * m2.values[k][j];
			}
			result.values[i][j] = v;
		}
	}
	return result;
}


Matrix4d Matrix4d::mn(const Matrix4d& m1, const double& num) {
	Matrix4d result;
	for (int i = 0; i < 4; i++)
	{
		for (int j = 0; j < 4; j++)
		{
			result.values[i][j] *= num;
		}
	}
	return result;
}


Vector4 Matrix4d::mv(const Matrix4d& m1, const Vector4& v) {
	Vector4 result = Vector4(
		m1.values[0][0] * v.x + m1.values[0][1] * v.y + m1.values[0][2] * v.z + m1.values[0][3] * v.w,
		m1.values[1][0] * v.x + m1.values[1][1] * v.y + m1.values[1][2] * v.z + m1.values[1][3] * v.w,
		m1.values[2][0] * v.x + m1.values[2][1] * v.y + m1.values[2][2] * v.z + m1.values[2][3] * v.w, 
		m1.values[3][0] * v.x + m1.values[3][1] * v.y + m1.values[3][2] * v.z + m1.values[3][3] * v.w);;
	return result;

}


Matrix4d Matrix4d::transpose() {
	double t = values[0][1]; values[0][1] = values[1][0]; values[1][0] = t;
	t = values[0][2]; values[0][2] = values[2][0]; values[2][0] = t;
	t = values[0][3]; values[0][3] = values[3][0]; values[3][0] = t;
	t = values[1][2]; values[1][2] = values[2][1]; values[2][1] = t;
	t = values[1][3]; values[1][3] = values[3][1]; values[3][1] = t;
	t = values[2][3]; values[2][3] = values[3][2]; values[3][2] = t;
	return *this;
}
