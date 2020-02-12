#include<stdio.h>
#include <fstream>
using namespace std;

int inputValues[128700];

ifstream inFile;
File *fp1;

int main() {

	inFile.open("bit_transfer_test.txt");

	fp1 = fopen("bit_list.bin", "w")

	// freopen("bit_transfer_test.txt", "r", stdin);

	if (!inFile) {
		cerr << "Unable to open bit transfer file.";
		exit(1);
	}

	int x;
	int idx = 0;

	while (inFile >> x) {
		inputValues[idx] = x;
		idx++;
	}

	inFile.close();

	for (int i = 0; i < idx+1; i++) {
		putc(inputValues[i], fp1)
	}

	fclose(fp1)
	
}