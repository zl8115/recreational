#include <fstream>
#include <iostream>
#include <string>
#include <cstring>
#include <vector>
#include <charconv>
#include <string_view>
#include <ranges>
#include <sstream>

bool IsP2 = false;

bool canSolve(std::size_t* arr, std::size_t size, std::size_t acc, const std::size_t target)
{
	if (size <= 0)
		return acc == target;
	if (acc > target)
		return false;

	std::size_t temp;
	if (temp = acc + arr[0]; temp >= acc)
		if (canSolve(&arr[1], size - 1, temp, target))
			return true;
	if (temp = acc * arr[0]; temp >= acc)
		if (canSolve(&arr[1], size - 1, temp, target))
			return true;

	if (IsP2)
	{
		std::ostringstream ss;
		ss << acc << arr[0];
		const std::string& s = ss.str();

		temp = 0;
		std::from_chars(s.data(), s.data() + s.size(), temp);
		if (temp > acc)
			if (canSolve(&arr[1], size - 1, temp, target))
				return true;
	}
	return false;
}

std::size_t solve(std::ifstream& input_stream)
{
	std::size_t ans = 0;
	for (std::string line; std::getline(input_stream, line);)
	{
		std::size_t value = 0;
		auto [ptr, _] = std::from_chars(line.data(), line.data() + line.size(), value);
		auto views = std::string_view(ptr + 2)
			| std::views::split(' ')
			| std::views::transform([](auto sv){return std::stoll(sv.data()); });
		std::vector<std::size_t> arr(views.begin(), views.end());
		if (canSolve(arr.data(), arr.size(), 0, value))
			ans += value;
	}
	return ans;
}

int main (int argc, char** argv)
{
	std::ifstream input_stream("Day7/input.txt");
	std::vector<std::string> input;

	IsP2 = (argc == 2 && std::strcmp(argv[1], "-p2") == 0);
	std::cout << solve(input_stream) << std::endl;
}

// p1: 3245122495150
// p2: 105517128211543
