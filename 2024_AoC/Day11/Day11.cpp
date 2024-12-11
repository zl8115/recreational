#include <fstream>
#include <iostream>
#include <string>
#include <cstring>
#include <ranges>
#include <format>
#include <map>
#include <algorithm>

class Solver
{
public:
	using inputT = std::string;
	using outputT = std::size_t;

	Solver(const std::string& input_path)
	{
		loadInput(input_path);
	}

	outputT solve(bool isP2 = false)
	{
		return isP2 ? p2() : p1();
	}

private:
	void loadInput(const std::string& path)
	{
		std::ifstream inputStream(path);
		std::string line;
		std::getline(inputStream, line);
		m_input = line;
	}

	outputT observeStones(int blinks = 25)
	{
		std::map<outputT, outputT, std::greater<outputT>> map;
		std::map<outputT, outputT, std::greater<outputT>> tmpMap;

		std::ranges::for_each(m_input | std::views::split(' '), [&map](auto rv){
			map[std::stoi(std::string(rv.data(), rv.size()))]++;
		});

		for (int ii = 0; ii < blinks; ++ii)
		{
			for (auto [k, v]: map)
			{
				if (v == 0)
					continue;
				else if (k == 0)
					tmpMap[1] += v;
				else if (std::string no = std::format("{}", k); no.size() % 2 == 0)
				{
					int midIdx = no.size()/2;
					outputT lIdx = std::stoi(no.substr(0, midIdx));
					outputT rIdx = std::stoi(no.substr(midIdx));
					tmpMap[lIdx] += v;
					tmpMap[rIdx] += v;
				}
				else
				{
					tmpMap[k*2024] += v;
				}
				map[k] = 0;
			}
			std::swap(map, tmpMap);
		}

		outputT ans = 0;
		for(auto& [k,v]: map)
		{
			// std::cout << k << "|" << v << std::endl;
			ans += v;
		}
		return ans;
	}

	outputT p1()
	{
		return observeStones();
	}

	outputT p2()
	{
		return observeStones(75);
	}

	inputT m_input;
};

int main(int argc, char** argv)
{
	Solver solver("Day11/input.txt");
	std::cout << solver.solve(argc == 2 && strcmp(argv[1], "-p2") == 0) << std::endl;
}

// p1: 213625
// p2: 252442982856820
