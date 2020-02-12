#include<stdio.h>
#include <fstream>
using namespace std;

int inputValues[128700];

ifstream inFile;
FILE *fp1;


int main() {

	inFile.open("bit_transfer.txt");

	fp1 = fopen("bit_list.bin", "w");

	if (!inFile) {
		printf("Unable to open bit transfer file.");
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
		putc(inputValues[i], fp1);
	}

	fclose(fp1);

	ifstream file("bit_list.bin", ios::binary | ios::ate);
	int uncompressedSize = file.tellg();

	//need to compress bit_list.bin and find size of that to get ratio
	
}