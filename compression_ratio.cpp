#include <stdio.h>
#include <fstream>
#include <string>
#include <string.h>
#include <cstring>
using namespace std;

int inputValues[128700];

ifstream inFile;
FILE *fp1;
ifstream fpCounter;
FILE *fileClear;

long long int findSize(char file_name[]) 
{ 
    // opening the file in read mode 
    FILE* filePoint = fopen(file_name, "r"); 
    // checking if the file exist or not 
    if (filePoint == NULL) { 
        printf("File Not Found!\n"); 
        return -1; 
    }
    fseek(filePoint, 0L, SEEK_END);
    // calculating the size of the file 
    long int res = ftell(filePoint); 
    // closing the file 
    fclose(filePoint); 
  
    return res; 
} 

int main() {

	inFile.open("bit_transfer.txt");

	fpCounter.open("counter.txt");

	int countingValue;
	fpCounter >> countingValue;

	char dest1[255];
	strcpy( dest1, "bin_files/bit_list_" );

	char const *put1 = to_string(countingValue+1).c_str();
	char put2[5] = ".bin";

	strcat(dest1, put1);
	strcat(dest1, put2);

	char dest1_copy[255];
	strcpy( dest1_copy, dest1);

	char file_folder_base[600];
	strcpy( file_folder_base, "bin_files/" );

	strcat(file_folder_base, dest1_copy);

	fp1 = fopen(file_folder_base, "w");
	
	fileClear = fopen("counter.txt", "w");
	putc(countingValue+1, fileClear);

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

	//printf("%i", idx);

	inFile.close();
	for (int i = 0; i < idx; i++) {
		putc( (char) inputValues[i], fp1);
	}

	fclose(fp1);

	// long long int origSize = findSize("bit_list.bin");
	
}