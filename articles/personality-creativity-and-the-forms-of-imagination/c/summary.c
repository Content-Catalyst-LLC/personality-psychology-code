#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE 1024

int main(void) {
    FILE *file = fopen("data/synthetic_personality_creativity.csv", "r");
    if (!file) {
        perror("Could not open data/synthetic_personality_creativity.csv");
        return 1;
    }

    char line[MAX_LINE];
    int row_count = 0;
    double openness_sum = 0.0;
    double divergent_sum = 0.0;
    double achievement_sum = 0.0;

    /* Skip header */
    fgets(line, sizeof(line), file);

    while (fgets(line, sizeof(line), file)) {
        char *token;
        int col = 0;
        double openness = 0.0;
        double divergent = 0.0;
        double achievement = 0.0;

        token = strtok(line, ",");
        while (token != NULL) {
            if (col == 2) openness = atof(token);
            if (col == 10) divergent = atof(token);
            if (col == 11) achievement = atof(token);
            token = strtok(NULL, ",");
            col++;
        }

        openness_sum += openness;
        divergent_sum += divergent;
        achievement_sum += achievement;
        row_count++;
    }

    fclose(file);

    if (row_count == 0) {
        fprintf(stderr, "No data rows found.\n");
        return 1;
    }

    printf("Rows: %d\n", row_count);
    printf("Mean openness: %.2f\n", openness_sum / row_count);
    printf("Mean divergent thinking: %.2f\n", divergent_sum / row_count);
    printf("Mean creative achievement: %.2f\n", achievement_sum / row_count);

    return 0;
}
