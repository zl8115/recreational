#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <cstring>
#include <array>
#include <set>
#include <numeric>
#include <format>

using coord = std::pair<int,int>;
coord operator+ (const coord& lhs, const coord& rhs)
{
	return coord{lhs.first + rhs.first, lhs.second + rhs.second};
}

coord operator- (const coord& lhs, const coord& rhs)
{
	return coord{lhs.first - rhs.first, lhs.second - rhs.second};
}

struct coordMinus
{
	coord operator()(const coord& lhs, const coord& rhs) const
	{
		return lhs - rhs;
	}
};

struct coordLess
{
	bool firstHasPrecedence = false;
	bool operator()(const coord& lhs, const coord& rhs) const
	{
		if (firstHasPrecedence)
		{
			if (lhs.first == rhs.first)
				return lhs.second < rhs.second;
			return lhs.first < rhs.first;
		}
		if (lhs.second == rhs.second)
			return lhs.first < rhs.first;
		return lhs.second < rhs.second;
	}
};

static constexpr std::array<coord, 4> Directions = {
	coord(0,-1),
	coord(0,1),
	coord(-1,0),
	coord(1,0)
};

class Solver
{
public:
	using inputT = std::vector<std::vector<char>>;
	using outputT = std::size_t;
	using areaPeriT = coord;

	Solver(const std::string& input_path)
	{
		for (int ii = 0; ii < Directions.size(); ++ii)
		{
			m_boundaries[ii] = std::set<coord,coordLess>(coordLess{Directions[ii].first != 0});
		}
		loadInput(input_path);
	}

	void printInput()
	{
		for (auto& r: m_input)
		{
			for (auto& c: r)
				std::cout << c << '|';
			std::cout << std::endl;
		}
	}

	outputT solve(bool isP2 = false)
	{
		outputT res = 0;
		for (int ii = 0; ii < Ys; ++ii)
			for (int jj = 0; jj < Xs; ++jj)
				if (!m_visitedInput[ii][jj])
				{
					resetBoundaries();
					auto[area, perimeter] = dfs(coord{ii,jj});
					if (!isP2)
					{
						res += area * perimeter;
						// std::cout
						// 	<< std::format("({},{}) {}: {}A {}P",ii,jj,m_input[ii][jj],area,perimeter)
						// 	<< std::endl;
					}
					else
					{
						outputT edges = countEdges();
						res += area * edges;
						// std::cout
						// 	<< std::format("({},{}) {}: {}A {}E",ii,jj,m_input[ii][jj],area,edges)
						// 	<< std::endl;
					}
				}
		return res;
	}

private:
	inline bool isInMap(const coord& pos)
	{
		return pos.first >= 0 && pos.first < Ys && pos.second >= 0 && pos.second < Xs;
	}

	void resetBoundaries()
	{
		for (auto& b: m_boundaries)
			b.clear();
	}

	std::pair<int,int> dfs(const coord& pos)
	{
		std::pair<int,int> res(0,0);
		if (!isInMap(pos) || m_visitedInput[pos.first][pos.second])
			return res;

		res.first = 1;
		m_visitedInput[pos.first][pos.second] = 1;

		char myChar = m_input[pos.first][pos.second];
		for (int ii = 0; ii < Directions.size(); ++ii)
		{
			coord nextPos = pos + Directions[ii];
			if (!isInMap(nextPos) || m_input[nextPos.first][nextPos.second] != myChar)
			{
				m_boundaries[ii].insert(pos);
				++res.second;
			}
			else
			{
				res = res + dfs(nextPos);
			}
		}
		return res;
	}

	outputT countEdges()
	{
		outputT res = 0;
		for (auto& b: m_boundaries)
		{
			if (b.empty())
				continue;

			std::vector<coord> diff;
			std::adjacent_difference(b.begin(), b.end(), std::back_inserter(diff), coordMinus{});

			diff.erase(diff.begin());
			outputT acc = 1;
			for (auto& d: diff)
			{
				if (b.key_comp().firstHasPrecedence)
					acc += (d.first != 0 || d.second != 1) ? 1 : 0;
				else
					acc += (d.first != 1 || d.second != 0) ? 1 : 0;
			}
			// std::cout << acc << std::endl;
			res += acc;
		}
		return res;
	}

	void loadInput(const std::string& path)
	{
		m_input.clear();
		std::ifstream inputStream(path);
		for (std::string line; std::getline(inputStream, line);)
		{
			m_input.emplace_back(line.begin(), line.end());
		}
		Ys = m_input.size();
		Xs = m_input.at(0).size();
		m_visitedInput = std::vector<std::vector<int>>(Ys, std::vector<int>(Xs, 0));
	}

	std::size_t Ys;
	std::size_t Xs;
	inputT m_input;
	std::vector<std::vector<int>> m_visitedInput;
	std::array<std::set<coord, coordLess>, 4> m_boundaries;
};

int main(int argc, char** argv)
{
	Solver solver("Day12/input.txt");
	// solver.printInput();
	// solver.solve(argc == 2 && strcmp(argv[1], "-p2") == 0);
	std::cout << solver.solve(argc == 2 && strcmp(argv[1], "-p2") == 0) << std::endl;
}

// p1: 1319878
// p2: 784982
