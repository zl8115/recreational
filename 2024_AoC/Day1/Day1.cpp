#include <fstream>
#include <iostream>
#include <cstring>
#include <vector>
#include <unordered_map>
#include <algorithm>

int p1Solve(std::ifstream& istream)
{
	std::vector<long> l1;
	l1.reserve(1000);
	std::vector<long> l2;
	l2.reserve(1000);
	while(!istream.eof())
	{
		long val1 = 0;
		long val2 = 0;
		istream >> val1 >> val2;
	
		l1.push_back(val1);
		l2.push_back(val2);
	}
	std::sort(l1.begin(), l1.end());
	std::sort(l2.begin(), l2.end());

	long long accumulator = 0;
	for(int ii = 0; ii < l1.size(); ++ii)
	{
		long val = std::abs(l1[ii] - l2[ii]);
		accumulator += val;
	}
	return accumulator;
}

int p2Solve(std::ifstream& istream)
{
	std::vector<long> l1;
	l1.reserve(1000);
	std::unordered_map<long, int> m2;

	while(!istream.eof())
	{
		long val1 = 0;
		long val2 = 0;
		istream >> val1 >> val2;
	
		l1.push_back(val1);
		m2[val2]++;
	}

	long long accumulator = 0;
	for (auto v : l1)
	{
		accumulator += v * m2[v];
	}
	return accumulator;
}

int main(int argc, char** argv)
{
    long res = 0;
    std::ifstream input_file("Day1/input.txt");

    if (argc == 1)
    {
		// p1Solve(input_file);
		// input_file >> res;
        std::cout << p1Solve(input_file) << std::endl;
    }
    else if (argc == 2 && strcmp(argv[1], "-p2") == 0)
    {
        std::cout << p2Solve(input_file) << std::endl;
    }
}
