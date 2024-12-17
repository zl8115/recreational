#include <fstream>
#include <iostream>
#include <numeric>
#include <string>
#include <vector>
#include <cstring>
#include <algorithm>
#include <charconv>
#include <array>
#include <format>
#include <set>

using coord = std::pair<int, int>;
coord operator+ (const coord& lhs, const coord& rhs)
{
	return coord{lhs.first + rhs.first, lhs.second + rhs.second};
}

coord operator- (const coord& lhs, const coord& rhs)
{
	return coord{lhs.first - rhs.first, lhs.second - rhs.second};
}

std::ostream& operator<< (std::ostream& ss, const coord& pos)
{
	return ss << std::format("({},{})", pos.first, pos.second);
}

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

struct coordMinus
{
	coord operator()(const coord& lhs, const coord& rhs) const
	{
		return lhs - rhs;
	}
};

constexpr std::size_t Xs = 101;
constexpr std::size_t Ys = 103;
constexpr std::size_t MidXs = (Xs - 1) / 2;
constexpr std::size_t MidYs = (Ys - 1) / 2;

class Robot
{
public:
	Robot(const coord& pos, const coord& vel):
		m_pos(pos),
		m_vel(vel)
	{}

	void move()
	{
		coord temp = m_pos + m_vel;
		temp.first = adjustPosValue(temp.first, Xs);
		temp.second = adjustPosValue(temp.second, Ys);
		m_pos = temp;
	}

	coord pos() const
	{
		return m_pos;
	}

	coord vel() const
	{
		return m_vel;
	}

private:
	coord::first_type adjustPosValue(coord::first_type value, std::size_t limit)
	{
		coord::first_type tmp = value;
		while (tmp < 0)
			tmp += limit;
		while (tmp >= limit)
			tmp -= limit;
		return tmp;
	}

	coord m_pos;
	coord m_vel;
};

class Solver
{
public:
	using inputT = std::vector<Robot>;
	using outputT = std::size_t;

	Solver(const std::string& input_path)
	{
		loadInput(input_path);
	}

	void printInput()
	{
		for (auto& robot: m_input)
		{
		   std::cout << robot.pos() << " " << robot.vel() << std::endl;
		}
	}

	void simulate(int iter)
	{
		for (int ii = 1; ii <= iter; ++ii)
			for (auto& robot: m_input)
				robot.move();
	}

	void printRobots()
	{
		std::vector<std::vector<int>> map(Ys, std::vector<int>(Xs, 0));
		for (auto& robot: m_input)
		{
			const coord& pos = robot.pos();
			++map[pos.second][pos.first];
		}

		for (auto& r: map)
		{
			for (auto& c: r)
			{
				if (c == 0)
					std::cout << '.';
				else
					std::cout << 'A';
			}
		   std::cout << std::endl;
		}
	}

	outputT solve(bool isP2 = false)
	{
		return !isP2 ? p1() : p2();
	}

private:
	void loadInput(const std::string& path)
	{
		std::ifstream inputStream(path);
		auto isDigitOrMinus = [](char c) -> bool{
			return c == '-' || std::isdigit(c);
		};

		for (std::string line; std::getline(inputStream, line);)
		{
			std::vector<int> entry;

			auto beg = line.begin();
			for (int ii = 0; ii < 4; ++ii)
			{
				auto iter = std::find_if(beg, line.end(), isDigitOrMinus);
				auto offset = std::distance(line.begin(), iter);

				int res;
				std::from_chars(line.data() + offset, line.data() + line.size(), res);
				entry.emplace_back(res);
				beg = std::find_if_not(iter, line.end(), isDigitOrMinus);
			}
			m_input.emplace_back(coord(entry[0],entry[1]), coord(entry[2],entry[3]));
		}
	}

	int quadrantPos(const coord& pos)
	{
		if (pos.first == MidXs || pos.second == MidYs)
			return -1;
		if (pos.first < MidXs)
		{
			if (pos.second < MidYs)
				return 0;
			return 1;
		}
		else
		{
			if (pos.second < MidYs)
				return 2;
			return 3;
		}
	}

	void incrementQuadrant(const coord& pos)
	{
		int quadrant = quadrantPos(pos);
		if (quadrant == -1)
			return;
		++m_quadrantCount[quadrant];
	}

	outputT p1()
	{
		simulate(100);
		for (auto& robot: m_input)
		{
			incrementQuadrant(robot.pos());
		}

		outputT res = 0;
		for (auto& count: m_quadrantCount)
			std::cout << count << " ";
		std::cout << std::endl;
		return m_quadrantCount[0] * m_quadrantCount[1] * m_quadrantCount[2] * m_quadrantCount[3];
	}

	outputT p2()
	{
		std::vector<int> candidates;
		auto tempRobots = m_input;
		std::pair<int, int> XMax;
		std::pair<int, int> YMax;
		for (int ii = 1; ii <= 100000; ++ii)
		{
			std::set<coord, coordLess> XSorter;
			std::set<coord, coordLess> YSorter(coordLess{true});
			for (auto& robot: tempRobots)
			{
				robot.move();
				const coord& pos = robot.pos();
				XSorter.insert(pos);
				YSorter.insert(pos);
			}

			std::vector<coord> diff;
			std::adjacent_difference(XSorter.begin(), XSorter.end(), std::back_inserter(diff), coordMinus{});

			std::size_t lineCount = 0;
			std::size_t largestLine = 0;
			coord prev = {0,0};
			for (auto& d: diff)
			{
				if (d.second != prev.second)
					lineCount = 0;
				++lineCount;
				prev = d;
				largestLine = std::max(largestLine, lineCount);
			}
			if (largestLine >= XMax.second)
				XMax = {ii, largestLine};

			lineCount = 0;
			largestLine = 0;
			prev = {0,0};
			diff.clear();

			std::adjacent_difference(YSorter.begin(), YSorter.end(), std::back_inserter(diff), coordMinus{});
			for (auto& d: diff)
			{
				if (d.first != prev.first)
					lineCount = 0;
				++lineCount;
				prev = d;
				largestLine = std::max(largestLine, lineCount);
			}

			if (largestLine >= YMax.second)
			{
				YMax = {ii, largestLine};
				if (YMax.first == XMax.first)
				{
					std::cout << std::format("Candidate iter {}: {} | {}", ii, XMax.second, YMax.second) << std::endl;
				}
			}
		}
		return XMax.first;
	}

	std::array<std::size_t, 4> m_quadrantCount = {0,0,0,0};
	inputT m_input;
};

int main(int argc, char** argv)
{
	Solver solver("Day14/input.txt");
	if (argc == 3 && strcmp(argv[1], "-s") == 0)
	{
		solver.simulate(std::stoi(argv[2]));
		solver.printRobots();
	}
	else
		std::cout << solver.solve(argc == 2 && strcmp(argv[1], "-p2") == 0) << std::endl;
}

// p1: 233709840
// p2: 6620
