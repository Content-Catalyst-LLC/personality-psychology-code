#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
int main(){ std::ifstream f("../data/synthetic_values_strivings_direction.csv"); std::string line; std::getline(f,line); int n=0; double sum=0;
while(std::getline(f,line)){ std::stringstream ss(line); std::string field; int col=0; while(std::getline(ss,field,',')){ if(col==28) sum += std::stod(field); col++; } n++; }
std::ofstream out("../outputs/cpp_values_strivings_summary.txt"); out<<"n="<<n<<"\nlife_direction_coherence_mean="<<sum/n<<"\n"; std::cout<<"Wrote C++ output.\n"; }
