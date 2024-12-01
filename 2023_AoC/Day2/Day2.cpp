#include <climits>
#include <iostream>
#include <algorithm>
#include <fstream>
#include <stdexcept>
#include <string>
#include <string_view>
#include <ranges>
#include <charconv>
#include <cstring>
#include <functional>

using CountType = std::array<int, 3>;

CountType CountCubes(std::string_view sv)
{
	static constexpr std::array<const char*, 3> Colors = {
		"red",
		"green",
		"blue"
	};

	CountType counts = {0,0,0};
	
	auto views = sv | std::ranges::views::split(' ');
	int value = INT_MAX;
	for (auto view: views)
	{
		auto [ptr, ec] = std::from_chars(view.data(), view.data() + view.size(), value);
		if (ec != std::errc())
		{
			auto iter = std::find_if(Colors.cbegin(), Colors.cend(), [&view](const auto c){return strncmp(view.data(), c, strlen(c)) == 0;});
			int index = std::distance(Colors.cbegin(), iter);
			counts.at(index) = std::max(value, counts.at(index));
		}
	}

	return counts;
}

int p1Solve(const std::string& line)
{
	auto pos = line.find(':');
	if (pos == std::string::npos) throw std::runtime_error("Colon not found");

	int gameId = 0;
	std::from_chars(line.data() + sizeof("Game"), line.data() + pos, gameId);

	std::string_view substr(line.begin() + pos + 2, line.end());
	// auto views = substr | std::ranges::views::split(' ');
	// std::cout << substr << std::endl;

	auto counts = CountCubes(substr);

	constexpr CountType MaxCounts = {12, 13, 14};
	for (int ii = 0; ii < MaxCounts.size(); ++ii)
	{
		if (counts[ii] > MaxCounts[ii]) return 0;
		// std::cout << count[ii];
	}
	// std::cout << std::endl;
	return gameId;
}

long p2Solve(const std::string& line)
{
	auto pos = line.find(':');
	if (pos == std::string::npos) throw std::runtime_error("Colon not found");
	std::string_view substr(line.begin() + pos + 2, line.end());
	auto counts = CountCubes(substr);

	// std::cout << counts[0] << counts[1] << counts[2] << std::endl;

	return counts[0] * counts[1] * counts[2];
}

int main(int argc, char** argv)
{
	long res = 0;

	std::ifstream input("Day2/input.txt");
	for(std::string line; std::getline(input, line);)
	{
		if (argc == 1)
		{
			res += p1Solve(line);
			// break;
		}
		else if(argc == 2 && strcmp(argv[1], "-p2") == 0)
		{
			res += p2Solve(line);
			// break;
		}
	}
	std::cout << res << std::endl;
}
