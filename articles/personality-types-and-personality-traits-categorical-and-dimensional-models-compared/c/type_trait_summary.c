#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAX_LINE 4096
int main(void){ FILE *fp=fopen("../data/synthetic_types_traits_dimensional_models.csv","r"); if(!fp){perror("data"); return 1;}
char line[MAX_LINE]; fgets(line,sizeof(line),fp); int n=0; int near=0;
while(fgets(line,sizeof(line),fp)){ char copy[MAX_LINE]; strncpy(copy,line,MAX_LINE); char *tok=strtok(copy,","); int col=0; while(tok){ if(col==13) near += atoi(tok); tok=strtok(NULL,","); col++; } n++; }
fclose(fp); FILE *out=fopen("../outputs/c_threshold_boundary_summary.txt","w"); fprintf(out,"n=%d\nnear_threshold_boundary_n=%d\nnear_threshold_boundary_rate=%.4f\n",n,near,(double)near/n); fclose(out); printf("Wrote C output.\n"); return 0; }
