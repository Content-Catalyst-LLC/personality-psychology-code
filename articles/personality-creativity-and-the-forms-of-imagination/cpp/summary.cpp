#include <fstream>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

std::vector<std::string> split_csv_line(const std::string& line) {
    std::vector<std::string> values;
    std::stringstream ss(line);
    std::string item;

    while (std::getline(ss, item, ',')) {
        values.push_back(item);
    }

    return values;
}

int main() {
    std::ifstream file("data/synthetic_personality_creativity.csv");
    if (!file.is_open()) {
        std::cerr << "Could not open data/synthetic_personality_creativity.csv\n";
        return 1;
    }

    std::string line;
    std::getline(file, line); // header

    int n = 0;
    double openness_sum = 0.0;
    double divergent_sum = 0.0;
    double achievement_sum = 0.0;

    while (std::getline(file, line)) {
        auto values = split_csv_line(line);
        if (values.size() < 12) {
            continue;
        }

        openness_sum += std::stod(values[2]);
        divergent_sum += std::stod(values[10]);
        achievement_sum += std::stod(values[11]);
        n++;
    }

    if (n == 0) {
        std::cerr << "No data rows found.\n";
        return 1;
    }

    std::cout << std::fixed << std::setprecision(2);
    std::cout << "Rows: " << n << "\n";
    std::cout << "Mean openness: " << openness_sum / n << "\n";
    std::cout << "Mean divergent thinking: " << divergent_sum / n << "\n";
    std::cout << "Mean creative achievement: " << achievement_sum / n << "\n";

    return 0;
}
