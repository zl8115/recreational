#include <fstream>
#include <iostream>
#include <cstring>
#include <string>
#include <string.h>
#include <charconv>

constexpr int ExprMaxLen = sizeof("mul(111,111)")/sizeof(char);

std::size_t evaluateMul(const char* substr, int maxIter)
{
    if (strncmp(substr, "mul(", 4))
    {
        return 0;
    }
    bool endFound = false;
    bool commaFound = false;
    auto firstArg = std::make_pair<int,int>(-1, -1);
    auto secondArg = std::make_pair<int,int>(-1, -1);
    bool isDigit = true;
    for (int jj = 4; jj < maxIter; ++jj)
    {
        const char c = *(substr + jj);
        if (std::isdigit(c))
        {
            if (firstArg.first == -1)
                firstArg.first = jj;

            if (firstArg.second != -1 && secondArg.first == -1)
                secondArg.first = jj;
        }
        else if (c == ')' && secondArg.first != -1)
        {
            if (secondArg.first != -1)
                secondArg.second = jj;
            else
                break;
        }
        else if (c == ',' && firstArg.first != -1)
        {
            if (firstArg.first != -1)
                firstArg.second = jj;
            else
                break;
        }
        else
        {
            break;
        }
    }
    if (firstArg.first == -1 || firstArg.second == -1 || secondArg.first == -1 || secondArg.second == -1)
        return 0;
    auto[s1, e1] = firstArg;
    auto[s2, e2] = secondArg;

    std::size_t v1 = 0, v2 = 0;
    std::from_chars(substr + s1, substr + e1, v1);
    std::from_chars(substr + s2, substr + e2, v2);
    return v1 * v2;
}

template<bool UseExtendedOper = false>
std::size_t solve(std::ifstream& istream)
{
    std::size_t ans = 0;
    bool disableOper = false;
    for(std::string line; std::getline(istream, line);)
    {
        for (int ii = 0; ii < line.size(); ++ii)
        {
            if constexpr (UseExtendedOper)
            {
                if (strncmp(&line[ii], "don't()", 7) == 0)
                    disableOper = true;
                else if (strncmp(&line[ii], "do()", 4) == 0)
                    disableOper = false;

                if (disableOper)
                    continue;
            }
            ans += evaluateMul(&line[ii], std::min<int>(line.size(), ii + ExprMaxLen));
        }
    }
    return ans;
}

int main(int argc, char** argv)
{
    std::ifstream input_file("Day3/input.txt");
    std::size_t ans = 0;

    if (argc == 1)
        ans += solve(input_file);
    else if (argc == 2 && strcmp(argv[1], "-p2") == 0)
        ans += solve<true>(input_file);
    std::cout << ans << std::endl;
}
