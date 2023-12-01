#include <string>
#include <fstream>
#include <algorithm>
#include <iostream>
#include <unordered_map>
#include <cstring>

inline bool IsDigit(const char c)
{
    return std::isdigit(c);
}

static const std::unordered_map<std::string, char> DigitWordMap {
    {"one", '1'},
    {"two", '2'},
    {"three", '3'},
    {"four", '4'},
    {"five", '5'},
    {"six", '6'},
    {"seven", '7'},
    {"eight", '8'},
    {"nine", '9'},
    {"zero", '0'},
};

char FindFirstDigit(std::string_view string)
{
    auto iter = std::find_if(string.begin(), string.end(), IsDigit);
    if (iter == string.end())
    {
        throw std::runtime_error("Could not find a digit in this string");
    }
    return *iter;
}

char FindLastDigit(std::string_view string)
{
    auto iter = std::find_if(string.rbegin(), string.rend(), IsDigit);
    if (iter == string.rend())
    {
        throw std::runtime_error("Could not find a digit in this string");
    }
    return *iter;
}

char FindFirstDigitNumberOrWord(std::string_view string)
{
    for (int ii = 0; ii < string.length(); ++ii)
    {
        if (IsDigit(string[ii]))
        {
            return string[ii];
        }
        std::string_view substr = string.substr(ii);
        auto iter = std::find_if(DigitWordMap.begin(), DigitWordMap.end(), [&substr](auto elm){return substr.starts_with(elm.first);});
        if (iter != DigitWordMap.end())
        {
            return iter->second;
        }
    }
    throw std::runtime_error("Could not find a digit in this string");
}

char FindLastDigitNumberOrWord(std::string_view string)
{
    for (int ii = string.length() -1; ii >= 0 ; --ii)
    {
        if (IsDigit(string[ii]))
        {
            return string[ii];
        }

        std::string_view substr = string.substr(ii);
        auto iter = std::find_if(DigitWordMap.begin(), DigitWordMap.end(), [&substr](auto elm){return substr.starts_with(elm.first);});
        if (iter != DigitWordMap.end())
        {
            return iter->second;
        }
    }
    throw std::runtime_error("Could not find a digit in this string");
}

int main(int argc, char** argv)
{
    bool isPart2 = false;
    if (argc > 1 && !strcmp(argv[1], "-p2"))
    {
        isPart2 = true;
    }

    std::ifstream input_file("input.txt");
    long accumulator = 0;
    for (std::string line; getline(input_file, line); )
    {
        char doubleDigit[2];
        if (!isPart2)
        {
            doubleDigit[0] = FindFirstDigit(line);
            doubleDigit[1] = FindLastDigit(line);
        }
        else
        {
            doubleDigit[0] = FindFirstDigitNumberOrWord(line);
            doubleDigit[1] = FindLastDigitNumberOrWord(line);
        }
        accumulator += std::stol(doubleDigit);
    }
    std::cout << accumulator << std::endl;
}