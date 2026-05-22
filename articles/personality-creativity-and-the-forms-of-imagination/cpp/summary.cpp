#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

int main() {
    std::ifstream file("../data/synthetic_personality_creativity.csv");
    if (!file.is_open()) {
        std::cerr << "could not open data file\n";
        return 1;
    }

    std::string line;
    std::getline(file, line); // header

    double openness_sum = 0.0;
    double everyday_sum = 0.0;
    int n = 0;

    while (std::getline(file, line)) {
        std::stringstream ss(line);
        std::string field;
        std::vector<std::string> fields;
        while (std::getline(ss, field, ',')) {
            fields.push_back(field);
        }
        openness_sum += std::stod(fields[1]);
        everyday_sum += std::stod(fields[12]);
        n++;
    }

    std::cout << "C++ summary utility\n";
    std::cout << "mean openness: " << openness_sum / n << "\n";
    std::cout << "mean everyday creativity: " << everyday_sum / n << "\n";
    return 0;
}
