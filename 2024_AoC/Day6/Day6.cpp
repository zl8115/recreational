#include <vector>
#include <fstream>
#include <iostream>
#include <utility>
#include <string>
#include <cstring>
#include <array>
#include <algorithm>
#include <unordered_map>

using coord = std::pair<int,int>;
coord operator+ (const coord& lhs, const coord& rhs)
{
	return coord{lhs.first + rhs.first, lhs.second + rhs.second};
}

struct coordHash
{
	size_t operator()(const coord& pos) const
	{
		return (static_cast<size_t>(pos.first) << 32 | pos.second);
	}
};

std::vector<std::string> gMap;
coord startPos;
int Ys;
int Xs;

constexpr std::array<coord, 4> Directions = {{
	{-1, 0},
	{0, 1},
	{1, 0},
	{0, -1}
}};

inline int incDirIdx(int dir)
{
	return (dir + 1) % Directions.size();
}

inline bool isValidPos(coord pos)
{
	return pos.first >= 0 && pos.first < Ys && pos.second >= 0 && pos.second < Xs;
}

inline int toBitMask(int dirIdx)
{
	return 1 << dirIdx;
}

void exploreObstruction(const coord& blockPos);

template<bool IsP2 = false>
int solve()
{
	int dirIdx = 0;
	std::vector<std::string> map = gMap;
	coord pos = startPos;
	map[pos.first][pos.second] = 'X';

	coord nextPos = pos;
	while(true)
	{
		coord nextPos = pos + Directions[dirIdx];
		// std::cout << nextPos.first << "|" << nextPos.second << std::endl;
		if (!isValidPos(pos + Directions[dirIdx]))
			break;
		else if (map[nextPos.first][nextPos.second] == '#')
		{
			dirIdx = (dirIdx + 1) % Directions.size();
			continue;
		}
		else
		{
			if constexpr(IsP2) exploreObstruction(nextPos);
			std::swap(pos, nextPos);
			map[pos.first][pos.second] = 'X';
		}
	}

	int ans = 0;
	if constexpr (!IsP2)
		std::for_each(map.begin(), map.end(), [&ans](auto& l){ans += std::ranges::count(l,'X');});
	else
		std::for_each(gMap.begin(), gMap.end(), [&ans](auto& l){ans += std::ranges::count(l,'O');});

	// std::cout << Ys << "|" << Xs << std::endl;
	// std::cout << startPos.first << "|" << startPos.second << std::endl;

	return ans;
}

void exploreObstruction(const coord& blockPos)
{
	std::unordered_map<coord, int, coordHash> visitedMap;

	int altDirIdx = 0;
	coord altPos = startPos;

	while(true)
	{
		coord nextPos = altPos + Directions[altDirIdx];
		if (!isValidPos(nextPos))
			break;

		if (visitedMap[nextPos] & toBitMask(altDirIdx))
		{
			gMap[blockPos.first][blockPos.second] = 'O';
			break;
		}
		else if (gMap[nextPos.first][nextPos.second] == '#' || nextPos == blockPos)
		{
			altDirIdx = incDirIdx(altDirIdx);
			visitedMap[altPos] |= toBitMask(altDirIdx);
		}
		else
		{
			visitedMap[nextPos] |= toBitMask(altDirIdx);
			std::swap(altPos, nextPos);
		}
	}
}

void loadMap()
{
	std::ifstream input_stream("Day6/input.txt");
	for (std::string line; std::getline(input_stream, line);)
	{
		if(auto pos = line.find('^'); pos != std::string::npos)
		{
			startPos = coord{gMap.size(), pos};
		}
		gMap.push_back(line);
	}
	Ys = gMap.size();
	Xs = gMap.back().size();
}

int main(int argc, char** argv)
{
	if (argc == 1)
	{
		loadMap();
		std::cout << solve() << std::endl;
	}
	else if (argc == 2 && strcmp(argv[1], "-p2") == 0)
	{
		loadMap();
		std::cout << solve<true>() << std::endl;
	}
}

// p1: 4722
// p2: 1602
