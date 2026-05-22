#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
    FILE *fp = fopen("../data/synthetic_personality_creativity.csv", "r");
    if (!fp) {
        perror("could not open data file");
        return 1;
    }

    char line[2048];
    fgets(line, sizeof(line), fp); /* header */

    int n = 0;
    double openness_sum = 0.0;
    double achievement_sum = 0.0;

    while (fgets(line, sizeof(line), fp)) {
        char *token;
        int col = 0;
        token = strtok(line, ",");
        while (token != NULL) {
            if (col == 1) openness_sum += atof(token);
            if (col == 11) achievement_sum += atof(token);
            token = strtok(NULL, ",");
            col++;
        }
        n++;
    }

    fclose(fp);
    printf("C summary utility\n");
    printf("mean openness: %.2f\n", openness_sum / n);
    printf("mean creative achievement: %.2f\n", achievement_sum / n);
    return 0;
}
