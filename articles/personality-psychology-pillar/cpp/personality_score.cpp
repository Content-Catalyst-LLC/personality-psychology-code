#include <iostream>

// Toy personality organization score.
// Compile with: g++ cpp/personality_score.cpp -o outputs/personality_score

int main() {
    double trait_stability = 0.78;
    double motivational_coherence = 0.72;
    double identity_integration = 0.68;
    double self_regulation = 0.74;
    double adaptive_flexibility = 0.63;
    double maladaptive_pressure = 0.22;

    double score =
        0.18 * trait_stability +
        0.16 * motivational_coherence +
        0.18 * identity_integration +
        0.18 * self_regulation +
        0.14 * adaptive_flexibility -
        0.20 * maladaptive_pressure;

    std::cout << "Personality organization score: " << score << "\n";
    return 0;
}
