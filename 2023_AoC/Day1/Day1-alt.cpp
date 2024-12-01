#include <cstring>
#include <algorithm>
#include <iostream>
#include <fstream>
#include <string>
#include <array>

int p1DecodeLine(const std::string& inputLine)
{
    auto iterFirst = std::find_if(inputLine.cbegin(), inputLine.cend(), static_cast<int(*)(int)>(std::isdigit));
    auto iterEnd = std::find_if(inputLine.crbegin(), inputLine.crend(), static_cast<int(*)(int)>(std::isdigit));

    char value[2] = {*iterFirst, *iterEnd};
    return std::stoi(value);
}

int p2DecodeLine(const std::string& inputLine)
{
    static const std::array<std::string, 20> DigitValues = {
        "zero", // technically not valid but meh
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
        "0", // technically not valid but meh
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9"
    };
    // std::cout << inputLine << std::endl;

    char res[2] = {'\0', '\0'};
    for(const char* ptr = inputLine.data(); *ptr != '\0'; ptr++)
    {
        auto iter = std::find_if(DigitValues.cbegin(), DigitValues.cend(), [ptr](const auto& str) { return strncmp(str.data(), ptr, str.size()) == 0; });
        if (iter != DigitValues.cend())
        {
            if (res[0] == '\0')
            {
                res[0] = '0' + (std::distance(DigitValues.cbegin(), iter) % 10 );
            }
            res[1] = '0' + (std::distance(DigitValues.cbegin(), iter) % 10 );
            // std::cout << *iter << std::endl;
        }
        // std::cout << ptr;
    }
    // std::cout << std::endl;
    // std::cout << first << " " << last << std::endl;

    // auto iterFirst = std::find_first_of(inputLine.cbegin(), inputLine.cend(), DigitValues.cbegin(), DigitValues.cend());
    return std::stoi(res);
}

int main(int argc, char** argv)
{
    long res = 0;
    std::ifstream input_file("Day1/input.txt");

    if (argc == 1)
    {
        for(std::string line; std::getline(input_file, line);)
        {
            res += p1DecodeLine(line);
        }
        std::cout << res << std::endl;
    }
    else if (argc == 2 && strcmp(argv[1], "-p2") == 0)
    {
        for(std::string line; std::getline(input_file, line);)
        {
            res += p2DecodeLine(line);
            // break;
        }
        std::cout << res << std::endl;
    }
}
