#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <cstring>
#include <format>
#include <unordered_map>
#include <algorithm>
#include <unordered_set>

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

struct coordHash
{
	size_t operator()(const coord& pos) const
	{
		return (static_cast<size_t>(pos.first) << 32 | pos.second);
	}
};

static const std::unordered_map<char, coord> DirectionsMap = {
	{'^', {-1, 0}},
	{'>', {0, 1}},
	{'v', {1, 0}},
	{'<', {0, -1}}
};

class Solver
{
public:
	using inputT = std::vector<std::vector<char>>;
	using outputT = std::size_t;

	Solver(const std::string& input_path)
	{
		loadInput(input_path);
	}

	void printBoard()
	{
		for (const auto& r: m_input)
		{
			for (auto c: r)
				std::cout << c;
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
		int ii = 0;
		for (std::string line; std::getline(inputStream, line);)
		{
			if (line.empty())
				break;
			if (auto offset = line.find('@'); offset != line.npos)
				m_pos = coord(ii, offset);
			m_input.emplace_back(line.begin(), line.end());
			++ii;
		}
		Ys = m_input.size();
		Xs = m_input.at(0).size();

		for (std::string line; std::getline(inputStream, line);)
		{
			for (auto c: line)
				m_input2.push_back(DirectionsMap.at(c));
		}
	}

	void expandInput()
	{
		m_inputSwap.clear();
		for (const auto& r: m_input)
		{
			decltype(m_input)::value_type newRow;
			for (auto c: r)
			{
				if (c == '#' || c == '.')
				{
					newRow.emplace_back(c);
					newRow.emplace_back(c);
				}
				else if (c == 'O')
				{
					newRow.emplace_back('[');
					newRow.emplace_back(']');
				}
				else
				{
					newRow.emplace_back(c);
					newRow.emplace_back('.');
				}
			}
			m_inputSwap.emplace_back(std::move(newRow));
		}
		std::swap(m_inputSwap, m_input);
		auto& posRow = m_input[m_pos.first];
		m_pos.second = std::distance(posRow.begin(), std::find(posRow.begin(), posRow.end(), '@'));
		Xs = m_input.at(0).size();
	}

	char& boardAt(const coord& pos)
	{
		return m_input[pos.first][pos.second];
	}
	
	char& swapAt(const coord& pos)
	{
		return m_inputSwap[pos.first][pos.second];
	}

	inline bool isInMap(const coord& pos)
	{
		return pos.first >= 0 && pos.first < Ys && pos.second >= 0 && pos.second < Xs;
	}

	inline bool isBox(const coord& pos)
	{
		return (boardAt(pos) == 'O' || boardAt(pos) == '[' || boardAt(pos) == ']');
	}

	inline bool dirIsHorizontal(const coord& dir)
	{
		return dir == DirectionsMap.at('<') || dir == DirectionsMap.at('>');
	}

	bool pushBlock(const coord& pos, const coord& dir)
	{
		// std::cout << pos << dir << std::endl;
		if (!isInMap(pos))
			return false;

		if (m_visited.contains(pos))
			return true;
		m_visited.insert(pos);

		if (!isBox(pos))
		{
			if (boardAt(pos) == '.')
				return true;
			return false;
		}

		coord nextPos = pos + dir;
		if (!isInMap(nextPos) || boardAt(nextPos) == '#')
			return false;

		std::optional<coord> optionalPos;
		bool res = true;
		if (!pushBlock(nextPos, dir))
			return false;
		swapAt(pos) = '.';
		swapAt(nextPos) = boardAt(pos);
		// std::swap(swapAt(pos), swapAt(nextPos));

		if (boardAt(pos) == '[' && !dirIsHorizontal(dir))
			optionalPos = pos + DirectionsMap.at('>');
		else if (boardAt(pos) == ']' && !dirIsHorizontal(dir))
			optionalPos = pos + DirectionsMap.at('<');
		if (optionalPos)
		{
			if(!pushBlock(optionalPos.value(), dir))
				return false;
			swapAt(optionalPos.value()) = '.';
			swapAt(optionalPos.value() + dir) = boardAt(optionalPos.value());
		}
		return true;
	}

	void simulate(const coord& dir)
	{
		coord nextPos = m_pos + dir;
		if (!isInMap(nextPos) || boardAt(nextPos) == '#')
			return;
		else if (isBox(nextPos))
		{
			m_visited.clear();
			m_inputSwap = m_input;
			if (!pushBlock(nextPos, dir))
				return;
			std::swap(m_inputSwap, m_input);
		}
		boardAt(m_pos) = '.';
		boardAt(nextPos) = '@';
		m_pos = nextPos;
	}

	outputT countBoxes()
	{
		outputT res = 0;
		for (int ii = 0; ii < Ys; ++ii)
			for (int jj = 0; jj < Xs; ++jj)
				if (boardAt({ii,jj}) == 'O' || boardAt({ii,jj}) == '[')
					res += 100 * ii + jj;
		return res;
	}

	outputT p1()
	{
		return solveImpl();
	}

	outputT p2()
	{
		expandInput();
		return solveImpl();
	}

	outputT solveImpl()
	{
		int ii = 0;
		// printBoard();
		for (auto& dir: m_input2)
		{
			simulate(dir);
			// std::cout << std::endl;
			// printBoard();
		}
		// printBoard();
		return countBoxes();
	}

	std::size_t Ys;
	std::size_t Xs;
	coord m_pos;
	inputT m_input;
	inputT m_inputSwap;
	std::unordered_set<coord, coordHash> m_visited;
	std::vector<coord> m_input2;
};

int main(int argc, char** argv)
{
	Solver solver("Day15/input.txt");
	std::cout << solver.solve(argc == 2 && strcmp(argv[1], "-p2") == 0) << std::endl;
}

// p1: 151578
// p2: 1516544
