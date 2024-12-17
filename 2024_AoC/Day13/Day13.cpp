#include <fstream>
#include <iostream>
#include <string>
#include <typeinfo>
#include <vector>
#include <cstring>
#include <tuple>
#include <algorithm>
#include <charconv>
#include <format>
#include <cstdint>
#include <cmath>
#include <set>

using coord = std::pair<long, long>;
coord operator+ (const coord& lhs, const coord& rhs)
{
	return coord{lhs.first + rhs.first, lhs.second + rhs.second};
}

coord operator- (const coord& lhs, const coord& rhs)
{
	return coord{lhs.first - rhs.first, lhs.second - rhs.second};
}

bool operator< (const coord& lhs, const coord& rhs)
{
	if (lhs.first < rhs.first || lhs.second < rhs.second)
		return true;
	if (lhs.first == rhs.first)
		return lhs.second < rhs.second;
	return lhs.first < rhs.first;
}

struct coordHash
{
	size_t operator()(const coord& pos) const
	{
		return (static_cast<size_t>(pos.first) << 32 | pos.second);
	}
};

std::ostream& operator<< (std::ostream& ss, const coord& pos)
{
	return ss << std::format("({},{})", pos.first, pos.second);
}

class Solver
{
public:
	using inputT = std::vector<std::tuple<coord, coord, coord>>;
	using outputT = void;

	Solver(const std::string& input_path)
	{
		loadInput(input_path);
	}

	void printInput()
	{
		for (auto& e: m_input)
		{
		   std::cout << std::get<0>(e) << " " << std::get<1>(e) << " " << std::get<2>(e) << std::endl;
		}
	}

	bool isWithinTolerance(double a)
	{
		double b = std::round(a);
		return std::abs(a - b) < 1e-3;
	}

	std::size_t linAlg(const std::tuple<coord,coord,coord>& entry)
	{
		const coord& refA = std::get<0>(entry);
		const coord& refB = std::get<1>(entry);
		const coord& prize = std::get<2>(entry);

		double det = (refA.first * refB.second) - (refA.second * refB.first);
		double scale = 1.0 / det;
		double invAa = scale * refB.second;
		double invAb = scale * (-refB.first);
		double invAc = scale * (-refA.second);
		double invAd = scale * refA.first;

		double x = invAa * prize.first + invAb * prize.second;
		double y = invAc * prize.first + invAd * prize.second;

		if (isWithinTolerance(x) && isWithinTolerance(y))
			return (std::lround(x) * 3) + std::lround(y);

		return 0;
	}

	std::size_t countCoins(const std::tuple<coord,coord,coord>& entry)
	{
		const coord& refA = std::get<0>(entry);
		const coord& refB = std::get<1>(entry);
		const coord& prize = std::get<2>(entry);

		coord dB = coord(0,0);
		std::size_t bCoins = 0;
		while(true)
		{
			coord dA = coord(0,0);
			std::size_t aCoins = 0;
			while(true)
			{
				coord sum = dA + dB;
				if (prize == sum)
				{
					return (aCoins * 3) + bCoins;
				}

				if (prize.first < sum.first || prize.second < sum.second)
					break;

				++aCoins;
				dA = dA + refA;
			}
			++bCoins;
			dB = dB + refB;

			if (prize.first < dB.first || prize.second < dB.second)
				break;
		}
		return 0;
	}

	outputT solve(bool isP2 = false)
	{
		std::size_t res = 0;
		for (auto& e: m_input)
		{
			if (isP2)
			{
				std::get<2>(e).first += 10000000000000;
				std::get<2>(e).second += 10000000000000;
			}
			std::size_t val = linAlg(e);
			res += val;
		}
		std::cout << res << std::endl;
		return;
	}

private:
	void loadInput(const std::string& path)
	{
		std::ifstream inputStream(path);
		while(!inputStream.eof())
		{
			std::vector<coord> entry;
			entry.reserve(3);
			for (int ii = 0; ii < 3; ++ii)
			{
				coord res(0,0);
				std::string line;
				std::getline(inputStream, line);

				auto iter = std::find_if(line.begin(), line.end(), [](char c){return std::isdigit(c);});
				auto offset = std::distance(line.begin(), iter);
				std::from_chars(line.data() + offset, line.data() + line.size(), res.first);

				iter = std::find_if_not(iter, line.end(), [](char c){return std::isdigit(c);});
				iter = std::find_if(iter, line.end(), [](char c){return std::isdigit(c);});
				offset = std::distance(line.begin(), iter);
				std::from_chars(line.data() + offset, line.data() + line.size(), res.second);
				entry.emplace_back(std::move(res));
			}
			m_input.emplace_back(entry[0], entry[1], entry[2]);
			std::string throwaway; std::getline(inputStream, throwaway);
		}
	}

	inputT m_input;
};

int main(int argc, char** argv)
{
	Solver solver("Day13/input.txt");
	solver.printInput();
	solver.solve(argc == 2 && strcmp(argv[1], "-p2") == 0);
}

// p1: 32026
// p2: 89013607072065
