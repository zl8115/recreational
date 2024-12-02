#include <fstream>
#include <iostream>
#include <cstring>
#include <numeric>
#include <ranges>
#include <string>
#include <vector>

bool isSafe(std::vector<int> values)
{
	std::adjacent_difference(values.begin(), values.end(), values.begin());

	bool isUnsafe = false;
	int sign = values[1] < 0;
	for (auto iter = std::next(values.begin()); iter < values.end(); ++iter)
	{
		int absDiff = std::abs(*iter); 
		int diffSign = (*iter < 0);
		isUnsafe |= (absDiff < 1 || absDiff > 3) || (diffSign != sign);
	}
	return !isUnsafe;
}

int p1Solve(std::ifstream& istream)
{
	int res = 0;
	for(std::string line; std::getline(istream, line);)
	{
		auto int_views = line | std::views::split(' ') | std::views::transform([](auto v) { 
			std::string s(v.data(), v.size());
			return std::stoi(s);
		});

		if (isSafe(std::vector<int>(int_views.begin(), int_views.end()))) ++res;
	}
	return res;
}

int p2Solve(std::ifstream& istream)
{
	int res = 0;
	int lines = 0;
	for(std::string line; std::getline(istream, line);)
	{
		auto int_views = line | std::views::split(' ') | std::views::transform([](auto v) { 
			std::string s(v.data(), v.size());
			return std::stoi(s);
		});

		std::vector<int> values(int_views.begin(), int_views.end());
		if (isSafe(values)) 
		{
			++res;
		}
		else 
		{
			for(int ii = 0; ii < values.size(); ++ii)
			{
				auto c = values;
				c.erase(c.begin() + ii);
				if (isSafe(c))
				{
					++res;
					break;
				}
			}
		}
	}
	return res;
}

int main(int argc, char** argv)
{
    std::ifstream input_file("Day2/input.txt");

    if (argc == 1)
    {
        std::cout << p1Solve(input_file)<< std::endl;
    }
    else if (argc == 2 && strcmp(argv[1], "-p2") == 0)
    {
		std::cout << p2Solve(input_file) << std::endl;
    }
}
