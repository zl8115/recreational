#include <fstream>
#include <iostream>
#include <iterator>
#include <string>
#include <unordered_set>
#include <array>
#include <vector>
#include <deque>
#include <cstring>
#include <ranges>

std::array<std::unordered_set<int>,100> gPageOrderRules;
std::vector<std::string> PuzzleEntries;
void LoadInput()
{
	std::ifstream input_stream("Day5/input.txt");
	std::vector<std::string> grid;
	for (std::string line; std::getline(input_stream, line);)
	{
		if (line.empty())
			break;

		auto int_views = line | std::views::split('|') | std::views::transform([](auto v) { 
			std::string s(v.data(), v.size());
			return std::stoi(s);
		});

		auto iterBeg = int_views.begin();
		int v1 = *iterBeg;
		int v2 = *(std::ranges::next(iterBeg, 1));
		gPageOrderRules[v2].insert(v1);
	}

	for (std::string line; std::getline(input_stream, line);)
	{
		PuzzleEntries.push_back(line);
	}
}

int p1Solve(const std::string& line)
{
	// std::cout << line << std::endl;
	auto int_views = line | std::views::split(',') | std::views::transform([](auto v) { 
		std::string s(v.data(), v.size());
		return std::stoi(s);
	});

	std::vector<int> input(int_views.begin(), int_views.end());
	std::unordered_set<int> miniSet;
	for (int ii = 0; ii < input.size(); ++ii)
	{
		int val = input[ii];
		// std::cout << val << std::endl;
		if (miniSet.contains(val))
			return 0;
		miniSet.insert(gPageOrderRules[val].begin(), gPageOrderRules[val].end());
	}
	return input[(input.size())/2];
}

// Haha, this is dumb and naive way to solve. Pretty slow but it works xD
int p2Solve(const std::string& line)
{
	// std::cout << line << std::endl;
	auto int_views = line | std::views::split(',') | std::views::transform([](auto v) { 
		std::string s(v.data(), v.size());
		return std::stoi(s);
	});

	std::deque<int> input(int_views.begin(), int_views.end());
	std::unordered_set<int> miniSet;
	bool isSolved = true;
	int iter = 0;
	do
	{
		++iter;
		if (!isSolved)
		{
			miniSet.clear();
			isSolved = true;
		}

		for (int ii = 0; ii < input.size(); ++ii)
		{
			int val = input[ii];
			// std::cout << val << std::endl;
			if (miniSet.contains(val))
			{
				isSolved = false;
				input.erase(std::next(input.begin(), ii));
				input.push_front(val);
				break;
			}
			miniSet.insert(gPageOrderRules[val].begin(), gPageOrderRules[val].end());
		}
	}while(!isSolved);

	return (iter > 1) ? input[(input.size())/2] : 0;
}

int main(int argc, char** argv)
{
	if (argc == 1)
	{
		LoadInput();
		int ans = 0;
		for (auto& line: PuzzleEntries)
		{
			ans += p1Solve(line);
		}
		std::cout << ans << std::endl;
	}
	else if (argc == 2 && strcmp(argv[1], "-p2") == 0)
	{
		LoadInput();
		int ans = 0;
		for (auto& line: PuzzleEntries)
		{
			ans += p2Solve(line);
		}
		std::cout << ans << std::endl;
	}
}
