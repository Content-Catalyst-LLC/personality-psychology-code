#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
int main(){ std::ifstream f("../data/synthetic_mbti_typology_vs_traits.csv"); std::string line; std::getline(f,line); int n=0; int changed=0;
while(std::getline(f,line)){ std::stringstream ss(line); std::string field; int col=0; while(std::getline(ss,field,',')){ if(col==20) changed += std::stoi(field); col++; } n++; }
std::ofstream out("../outputs/cpp_mbti_type_change_summary.txt"); out<<"n="<<n<<"\ntype_changed_on_retest_n="<<changed<<"\ntype_change_rate="<<(double)changed/n<<"\n"; std::cout<<"Wrote C++ output.\n"; }
