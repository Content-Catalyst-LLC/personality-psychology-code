#include <stdio.h>

// Toy trait-expression probability utility.
// Compile with: cc c/trait_expression.c -o outputs/trait_expression

double latent_expression(double disposition, double goal, double context, double identity, double cost) {
    return 0.20 + 0.25 * disposition + 0.20 * goal + 0.20 * context + 0.20 * identity - 0.25 * cost;
}

int main(void) {
    double z = latent_expression(0.80, 0.70, 0.60, 0.75, 0.20);
    printf("Latent trait-expression score: %.3f\n", z);
    return 0;
}
