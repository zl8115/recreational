#include <fstream>
#include <iostream>
#include <unordered_map>
#include <unordered_set>
#include <vector>
#include <string>
#include <cstring>

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

std::vector<std::string> load_input(const std::string& input_path)
{
	std::vector<std::string> input_grid;
	std::ifstream input_stream(input_path);
	for (std::string line; std::getline(input_stream, line);)
	{
		input_grid.push_back(line);
	}
	return input_grid;
}

std::unordered_map<char, std::vector<coord>> load_map(const std::vector<std::string>& input_grid)
{
	std::unordered_map<char, std::vector<coord>> antennaMap;
	for (int ii = 0; ii < input_grid.size(); ++ii)
	{
		const std::string& line = input_grid.at(ii);
		for (int jj = 0; jj < line.size(); ++jj)
		{
			if (char c = line[jj]; c != '.')
				antennaMap[c].emplace_back(coord{ii, jj});
		}
	}
	return antennaMap;
}

inline bool IsInGrid(const coord pos, std::size_t Ys, std::size_t Xs)
{
	return (pos.first >= 0 && pos.first < Ys && pos.second >= 0 && pos.second < Xs);
}

bool IsP2 = false;
int solve(const std::vector<std::string>& inputGrid)
{
	const std::size_t Ys = inputGrid.size();
	const std::size_t Xs = inputGrid.at(0).size();

	auto antennaMap = load_map(inputGrid);
	std::unordered_set<coord, coordHash> antiNodeCoords;
	for(auto& [c, v]: antennaMap)
	{
		for(int ii = 0; ii < v.size(); ++ii)
		{
			for(int jj = ii + 1; jj < v.size(); ++jj)
			{
				coord diff = v[jj] - v[ii];

				coord pos = v[ii];
				coord temp = v[ii] - diff;
				if (IsP2)
				{
					antiNodeCoords.insert(v[ii]);
					antiNodeCoords.insert(v[jj]);
				}

				while(true)
				{
					temp = pos - diff;
					if (!IsInGrid(temp, Ys, Xs))
						break;
					antiNodeCoords.insert(temp);
					pos = temp;

					if (!IsP2)
						break;
				}
				
				pos = v[jj];
				while(true)
				{
					temp = pos + diff;
					if (!IsInGrid(temp, Ys, Xs))
						break;
					antiNodeCoords.insert(temp);
					pos = temp;

					if (!IsP2)
						break;
				}
			}
		}
	}

	// auto copyGrid = inputGrid;
	// for (auto& c: antiNodeCoords)
	// {
	// 	copyGrid[c.first][c.second] = '#';
	// }
	// for (auto& l: copyGrid)
	// {
	// 	std::cout << l << std::endl;
	// }

	return antiNodeCoords.size();
}

int main (int argc, char** argv)
{
	IsP2 = (argc == 2 && std::strcmp(argv[1], "-p2") == 0);
	auto inputGrid = load_input("Day8/input.txt");
	std::cout << solve(inputGrid) << std::endl;
}

// p1: 327
// p2: 1233
