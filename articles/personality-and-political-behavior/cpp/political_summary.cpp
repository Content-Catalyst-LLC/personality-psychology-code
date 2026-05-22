#include <fstream>
#include <iostream>
#include <sstream>
#include <string>

int main() {
    std::ifstream file("../data/synthetic_personality_political_behavior.csv");
    if (!file.is_open()) {
        std::cerr << "Could not open data file\n";
        return 1;
    }

    std::string line;
    std::getline(file, line); // header

    int n = 0;
    double participation_sum = 0.0;

    while (std::getline(file, line)) {
        std::stringstream ss(line);
        std::string field;
        int col = 0;

        while (std::getline(ss, field, ',')) {
            if (col == 15) {
                participation_sum += std::stod(field);
            }
            col++;
        }
        n++;
    }

    if (n == 0) {
        std::cerr << "No rows\n";
        return 1;
    }

    std::ofstream out("../outputs/cpp_political_summary.txt");
    out << "n=" << n << "\n";
    out << "political_participation_mean=" << participation_sum / n << "\n";

    std::cout << "Wrote C++ output: ../outputs/cpp_political_summary.txt\n";
    return 0;
}
