#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <cstring>
#include <algorithm>
#include <unordered_set>

using coord = std::pair<int,int>;
coord operator+ (const coord& lhs, const coord& rhs)
{
	return coord{lhs.first + rhs.first, lhs.second + rhs.second};
}

coord operator- (const coord& lhs, const coord& rhs)
{
	return coord{lhs.first - rhs.first, lhs.second - rhs.second};
}

struct coordHash
{
	size_t operator()(const coord& pos) const
	{
		return (static_cast<size_t>(pos.first) << 32 | pos.second);
	}
};

class Solver
{
public:
	using inputT = std::vector<std::vector<int>>;
	using outputT = int;

	Solver(const std::string& input_path)
	{
		loadInput(input_path);
	}

	void printInput()
	{
		for (auto&r: m_visitedInput)
		{
			for (auto& c: r)
			{
				if (c==-1)
					std::cout << '.' << '|';
				else
					std::cout << c << '|';
			}
		}
	}

	outputT solve(bool isP2 = false)
	{
		return isP2 ? p2() : p1();
	}

private:
	void loadInput(const std::string& path)
	{
		m_input.clear();
		std::ifstream inputStream(path);
		for (std::string line; std::getline(inputStream, line);)
		{
			char tmp[2] = {0,0};
			std::vector<int> entry;
			std::transform(line.begin(), line.end(), std::back_inserter(entry), [&tmp](auto c){
				if (!std::isdigit(c))
					return -1;
				tmp[0] = c;
				return std::atoi(tmp);
			});
			m_input.emplace_back(entry);
		}
		Ys = m_input.size();
		Xs = m_input.at(0).size();
		m_visitedInput = inputT(Ys, std::vector<int>(Xs,-1));
	}

	inline bool isInMap(const coord& pos)
	{
		return pos.first >= 0 && pos.first < Ys && pos.second >= 0 && pos.second < Xs;
	}

	void p1Hike(const coord& pos, std::unordered_set<coord, coordHash>& seenSet, int expectedVal)
	{
		if (expectedVal > 9 || !isInMap(pos) || m_input[pos.first][pos.second] != expectedVal)
			return;

		if (m_input[pos.first][pos.second] == 9)
		{
			seenSet.insert(pos);
			return;
		}
		p1Hike(pos + coord(1,0), seenSet, expectedVal + 1);
		p1Hike(pos + coord(-1,0), seenSet, expectedVal + 1);
		p1Hike(pos + coord(0,1), seenSet, expectedVal + 1);
		p1Hike(pos + coord(0,-1), seenSet, expectedVal + 1);
	}

	outputT p1()
	{
		outputT res = 0;
		for (int ii = 0; ii < Ys; ++ii)
			for (int jj = 0; jj < Xs; ++jj)
				if (m_input[ii][jj] == 0)
				{
					std::unordered_set<coord,coordHash> seenSet;
					p1Hike({ii,jj}, seenSet, 0);
					res += seenSet.size();
				}
		return res;
	}

	outputT p2Hike(const coord& pos, int expectedVal)
	{
		if (expectedVal > 9 || !isInMap(pos) || m_input[pos.first][pos.second] != expectedVal)
			return 0;
		else if (m_input[pos.first][pos.second] == 9)
			return 1;
		else if (int val = m_visitedInput[pos.first][pos.second]; val != -1)
			return val;

		int acc = 0;
		acc += p2Hike(pos + coord(1,0), expectedVal + 1);
		acc += p2Hike(pos + coord(-1,0), expectedVal + 1);
		acc += p2Hike(pos + coord(0,1), expectedVal + 1);
		acc += p2Hike(pos + coord(0,-1), expectedVal + 1);

		m_visitedInput[pos.first][pos.second] = acc;
		return acc;
	}

	outputT p2()
	{
		outputT res = 0;
		for (int ii = 0; ii < Ys; ++ii)
			for (int jj = 0; jj < Xs; ++jj)
				if (m_input[ii][jj] == 0)
				{
					p2Hike({ii,jj}, 0);
					res += m_visitedInput[ii][jj];
				}
		return res;
	}

	std::size_t Ys;
	std::size_t Xs;
	inputT m_input;
	inputT m_visitedInput;
};

int main(int argc, char** argv)
{
	Solver solver("Day10/input.txt");
	solver.solve(argc == 2 && strcmp(argv[1], "-p2") == 0);
	std::cout << solver.solve(argc == 2 && strcmp(argv[1], "-p2") == 0) << std::endl;
}

// p1: 644
// p2: 1366
