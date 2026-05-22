#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
int main(){ std::ifstream f("../data/synthetic_traits_character_morality.csv"); std::string line; std::getline(f,line); int n=0; double sum=0;
while(std::getline(f,line)){ std::stringstream ss(line); std::string field; int col=0; while(std::getline(ss,field,',')){ if(col==16) sum += std::stod(field); col++; } n++; }
std::ofstream out("../outputs/cpp_traits_character_summary.txt"); out<<"n="<<n<<"\nmoral_character_index_mean="<<sum/n<<"\n"; std::cout<<"Wrote C++ output.\n"; }
