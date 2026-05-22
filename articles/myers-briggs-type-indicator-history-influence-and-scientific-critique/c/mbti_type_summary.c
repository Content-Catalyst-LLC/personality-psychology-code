#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAX_LINE 4096
int main(void){ FILE *fp=fopen("../data/synthetic_mbti_typology_vs_traits.csv","r"); if(!fp){perror("data"); return 1;}
char line[MAX_LINE]; fgets(line,sizeof(line),fp); int n=0; int changed=0;
while(fgets(line,sizeof(line),fp)){ char copy[MAX_LINE]; strncpy(copy,line,MAX_LINE); char *tok=strtok(copy,","); int col=0; while(tok){ if(col==20) changed += atoi(tok); tok=strtok(NULL,","); col++; } n++; }
fclose(fp); FILE *out=fopen("../outputs/c_mbti_type_change_summary.txt","w"); fprintf(out,"n=%d\ntype_changed_on_retest_n=%d\ntype_change_rate=%.4f\n",n,changed,(double)changed/n); fclose(out); printf("Wrote C output.\n"); return 0; }
