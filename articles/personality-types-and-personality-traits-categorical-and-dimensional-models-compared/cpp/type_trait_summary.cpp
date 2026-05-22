#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
int main(){ std::ifstream f("../data/synthetic_types_traits_dimensional_models.csv"); std::string line; std::getline(f,line); int n=0; int near=0;
while(std::getline(f,line)){ std::stringstream ss(line); std::string field; int col=0; while(std::getline(ss,field,',')){ if(col==15) near += std::stoi(field); col++; } n++; }
std::ofstream out("../outputs/cpp_cluster_boundary_summary.txt"); out<<"n="<<n<<"\nnear_cluster_boundary_n="<<near<<"\nnear_cluster_boundary_rate="<<(double)near/n<<"\n"; std::cout<<"Wrote C++ output.\n"; }
