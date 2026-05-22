#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE 4096

int main(void) {
    FILE *fp = fopen("../data/synthetic_personality_work_leadership.csv", "r");
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
    double performance_sum = 0.0;

    while (fgets(line, sizeof(line), fp)) {
        char *token;
        int col = 0;
        token = strtok(line, ",");
        while (token != NULL) {
            if (col == 12) {
                performance_sum += atof(token);
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

    FILE *out = fopen("../outputs/c_work_leadership_summary.txt", "w");
    if (!out) {
        perror("Could not open output file");
        return 1;
    }

    fprintf(out, "n=%d\njob_performance_mean=%.4f\n", n, performance_sum / n);
    fclose(out);

    printf("Wrote C output: ../outputs/c_work_leadership_summary.txt\n");
    return 0;
}
