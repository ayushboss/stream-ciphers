#include <random>
#include <vector>
using namespace std;

linear_congruential_engine generator;
uniform_int_distribution<int> distribution(0,1);

vector<int> vals;

int main() {
	int numVals = 1029000;
	for (int i = 0; i < numVals; i++) {
		int tempVal = distribution(generator);
		vals.push_back(tempVal);
	}
}