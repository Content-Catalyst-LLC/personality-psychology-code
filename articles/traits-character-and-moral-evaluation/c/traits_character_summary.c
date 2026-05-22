#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAX_LINE 4096
int main(void){ FILE *fp=fopen("../data/synthetic_traits_character_morality.csv","r"); if(!fp){perror("data"); return 1;}
char line[MAX_LINE]; fgets(line,sizeof(line),fp); int n=0; double sum=0.0;
while(fgets(line,sizeof(line),fp)){ char *tok=strtok(line,","); int col=0; while(tok){ if(col==16) sum+=atof(tok); tok=strtok(NULL,","); col++; } n++; }
fclose(fp); FILE *out=fopen("../outputs/c_traits_character_summary.txt","w"); fprintf(out,"n=%d\nmoral_character_index_mean=%.4f\n",n,sum/n); fclose(out); printf("Wrote C output.\n"); return 0; }
