#include<iostream>
#include<fstream>
#include<string>

using namespace std;


void readFile(string fileName) {
	ifstream infile(fileName);
	if (!infile) {
		cout << "Failed to get file.\n";
	}

	string dataInfo;
	getline(infile, dataInfo);
	cout << dataInfo;

}


int main() {
	readFile("house.d.txt");
	 
}