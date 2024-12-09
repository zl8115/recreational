#include <fstream>
#include <iostream>
#include <vector>
#include <string>
#include <cstring>
#include <utility>
#include <list>

bool IsP2 = false;

std::string load_input(const std::string& input_path)
{
	std::ifstream input_stream(input_path);
	std::string line;
	std::getline(input_stream, line);
	return line;
}

std::vector<std::pair<int,int>> p1Refrag(std::vector<int>& data, std::vector<int>& empty)
{
	std::vector<std::pair<int, int>> res;
	int emptyIdx = 0;
	int emptySize = 0;

	for(int ii = 0; ii < data.size(); ++ii)
	{
		res.emplace_back(ii, data[ii]);
		data[ii] = 0;

		int emptySize = empty[ii];
		while(emptySize > 0 && data.back() > 0)
		{
			if (emptySize >= data.back())
			{
				res.emplace_back(data.size() - 1, data.back());
				emptySize -= data.back();
				data.pop_back();
			}
			else
			{
				res.emplace_back(data.size() - 1, emptySize);
				data.back() -= emptySize;
				emptySize = 0;
			}
		}
	}
	return res;
}

struct DataBlock
{
	int id;
	int size;
	DataBlock* next;
	DataBlock* prev;
};

void print(DataBlock* head)
{
	DataBlock* print = head;
	while(print)
	{
		char c = (print->id == -1) ? '.' : '0' + print->id;
		std::cout << std::string(print->size, c);
		print = print->next;
	}
	std::cout << std::endl;
}

void cpNode(DataBlock* src, DataBlock* dest)
{
	DataBlock* tmp;

	tmp = dest->prev;
	dest->prev = new DataBlock{src->id, src->size, dest, tmp};
	tmp->next = dest->prev;
}

void delNode(DataBlock* node)
{
	if (node->prev)
		node->prev->next = node->next;

	if (node->next)
		node->next->prev = node->prev;

	delete node;
}

std::vector<std::pair<int,int>> p2Refrag(std::vector<int>& data, std::vector<int>& empty)
{
	DataBlock dummy{-2,0,nullptr,nullptr};
	DataBlock* cur = &dummy; 
	for (int ii = 0; ii < data.size(); ++ii)
	{
		cur->next = new DataBlock{ii, data[ii], nullptr, cur};
		cur = cur->next;
		if (ii < empty.size())
		{
			cur->next = new DataBlock{-1, empty[ii], nullptr, cur};
			cur = cur->next;
		}
	}

	DataBlock* head = dummy.next;
	head->prev = nullptr;

	// print(head);
	DataBlock* cmp = nullptr;
	while(cur->prev)
	{
		if (cur->id == -1)
		{
			cur = cur->prev;
			continue;
		}
		if (cur->id != -1)
		{
			cmp = head;
			while(cmp && cmp != cur)
			{
				if (cmp->id == -1 && cmp->size >= cur->size)
				{
					DataBlock* nextNode = cur->prev;
					cpNode(cur, cmp);
					cmp->size -= cur->size;
					if (cmp->size == 0)
						delNode(cmp);
					cur->id = -1;

					cur = nextNode;
					break;
				}
				cmp = cmp->next;
			}
			// print(head);
		}
		cur = cur->prev;
	}

	std::vector<std::pair<int, int>> res;
	cur = head;
	while(cur)
	{
		if (cur->id == -1)
			res.emplace_back(0, cur->size);
		else
			res.emplace_back(cur->id, cur->size);

		DataBlock* tmp = cur->next;
		delete cur;

		cur = tmp;
	}
	return res;
}

std::size_t solve(const std::string& input)
{
	std::vector<int> data;
	std::vector<int> empty;
	
	char temp[2] = {0, 0};
	for (int ii = 0; ii < input.size(); ++ii)
	{
		temp[0] = input.at(ii);
		data.push_back(std::atoi(temp));
		std::swap(data, empty);
	}
	if (input.size() % 2 != 0)
		std::swap(data, empty);

	std::vector<std::pair<int,int>> res;
	if (!IsP2)
		res = p1Refrag(data, empty);
	else
		res = p2Refrag(data, empty);
	
	std::size_t ans = 0;
	std::size_t index = 0;
	for (auto& [id, rng]: res)
	{
		for(int ii = 0; ii < rng; ++ii)
		{
			ans += index * id;
			++index;
		}
	}

	return ans;
}

int main (int argc, char** argv)
{
	IsP2 = (argc == 2 && std::strcmp(argv[1], "-p2") == 0);
	auto input = load_input("Day9/input.txt");
	std::cout << solve(input) << std::endl;
}

// p1: 6259790630969
// p2: 6289564433984
