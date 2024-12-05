#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <cstring>

std::size_t Xs = 0;
std::size_t Ys = 0;

template <bool IsReversed>
int countWordInstanceBelow(const std::vector<std::string>& grid, int y, int x)
{
	const char* Word = IsReversed ? "SAMX" : "XMAS";
	
	const bool CanLeft = x - 3 >= 0;
	const bool CanRight = x + 3 < Xs;
	const bool CanDown = y + 3 < Ys;

	int ans = 0;
	if (CanRight &&
		grid[y][x] == Word[0] &&
		grid[y][x+1] == Word[1] &&
		grid[y][x+2] == Word[2] &&
		grid[y][x+3] == Word[3])
	{
		// std::cout << "Right " << y << " " << x << std::endl;
		++ans;
	}

	if (CanDown &&
		grid[y][x] == Word[0] &&
		grid[y+1][x] == Word[1] &&
		grid[y+2][x] == Word[2] &&
		grid[y+3][x] == Word[3])
	{
		// std::cout << "Down " << y << " " << x << std::endl;
		++ans;
	}

	if (CanLeft &&
		CanDown &&
		grid[y][x] == Word[0] &&
		grid[y+1][x-1] == Word[1] &&
		grid[y+2][x-2] == Word[2] &&
		grid[y+3][x-3] == Word[3])
	{
		// std::cout << "DownLeft " << y << " " << x << std::endl;
		++ans;
	}
	
	if (CanRight &&
		CanDown &&
		grid[y][x] == Word[0] &&
		grid[y+1][x+1] == Word[1] &&
		grid[y+2][x+2] == Word[2] &&
		grid[y+3][x+3] == Word[3])
	{
		// std::cout << "DownRight " << y << " " << x << std::endl;
		++ans;
	}
	return ans;
}

int p1Solve(const std::vector<std::string>& grid)
{
	int ans = 0;
	for (int ii = 0; ii < Ys; ++ii)
	{
		for (int jj = 0; jj < Xs; ++jj)
		{
			if (grid[ii][jj] == 'X')
				ans += countWordInstanceBelow<false>(grid, ii, jj);
			else if (grid[ii][jj] == 'S')
				ans += countWordInstanceBelow<true>(grid, ii , jj);
		}
	}
	return ans;
}

int countXMas(const std::vector<std::string>& grid, int y, int x)
{
	if (x < 1 || x >= Xs - 1 || y < 1 || y >= Ys - 1)
		return 0;

	constexpr char Word[] = "MAS";
	
	int ans = 0;
	if (grid[y-1][x-1] == Word[0] &&
		grid[y][x] == Word[1] &&
		grid[y+1][x+1] == Word[2] &&
		grid[y-1][x+1] == Word[2] &&
		grid[y+1][x-1] == Word[0])
	{
		// std::cout << "MAS-MAS " << y << " " << x << std::endl;
		++ans;
	}

	if (grid[y-1][x-1] == Word[0] &&
		grid[y][x] == Word[1] &&
		grid[y+1][x+1] == Word[2] &&
		grid[y-1][x+1] == Word[0] &&
		grid[y+1][x-1] == Word[2])
	{
		// std::cout << "MAS-SAM " << y << " " << x << std::endl;
		++ans;
	}

	if (grid[y-1][x-1] == Word[2] &&
		grid[y][x] == Word[1] &&
		grid[y+1][x+1] == Word[0] &&
		grid[y-1][x+1] == Word[0] &&
		grid[y+1][x-1] == Word[2])
	{
		// std::cout << "SAM-SAM " << y << " " << x << std::endl;
		++ans;
	}

	if (grid[y-1][x-1] == Word[2] &&
		grid[y][x] == Word[1] &&
		grid[y+1][x+1] == Word[0] &&
		grid[y-1][x+1] == Word[2] &&
		grid[y+1][x-1] == Word[0])
	{
		// std::cout << "SAM-MAS " << y << " " << x << std::endl;
		++ans;
	}
	return ans;
}

int p2Solve(const std::vector<std::string>& grid)
{
	int ans = 0;
	for (int ii = 0; ii < Ys; ++ii)
	{
		for (int jj = 0; jj < Xs; ++jj)
		{
			if (grid[ii][jj] == 'A')
				ans += countXMas(grid, ii, jj);
		}
	}
	return ans;
}

int main(int argc, char** argv)
{
	std::ifstream input_stream("Day4/input.txt");
	std::vector<std::string> grid;
	for (std::string line; std::getline(input_stream, line);)
	{
		grid.push_back(line);
	}
	Ys = grid.size();
	Xs = grid.size();

	if (argc == 1)
	{
		std::cout << p1Solve(grid) << std::endl;
	}
	else if (argc == 2 && strcmp(argv[1], "-p2") == 0)
	{
		std::cout << p2Solve(grid) << std::endl;
	}
}
