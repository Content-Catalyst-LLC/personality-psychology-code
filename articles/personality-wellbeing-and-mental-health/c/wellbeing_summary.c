#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE 4096

int main(void) {
    FILE *fp = fopen("../data/synthetic_personality_wellbeing_mental_health.csv", "r");
    if (!fp) {
        perror("Could not open data file");
        return 1;
    }

    char line[MAX_LINE];
    if (!fgets(line, sizeof(line), fp)) {
        fprintf(stderr, "Missing header\n");
        fclose(fp);
        return 1;
    }

    int n = 0;
    double wellbeing_sum = 0.0;

    while (fgets(line, sizeof(line), fp)) {
        char *token;
        int col = 0;
        token = strtok(line, ",");
        while (token != NULL) {
            if (col == 15) {
                wellbeing_sum += atof(token);
            }
            token = strtok(NULL, ",");
            col++;
        }
        n++;
    }

    fclose(fp);

    if (n == 0) {
        fprintf(stderr, "No rows\n");
        return 1;
    }

    FILE *out = fopen("../outputs/c_wellbeing_summary.txt", "w");
    if (!out) {
        perror("Could not open output file");
        return 1;
    }

    fprintf(out, "n=%d\nwellbeing_score_mean=%.4f\n", n, wellbeing_sum / n);
    fclose(out);

    printf("Wrote C output: ../outputs/c_wellbeing_summary.txt\n");
    return 0;
}
