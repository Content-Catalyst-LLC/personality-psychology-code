#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
int main(){ std::ifstream f("../data/synthetic_narrative_identity.csv"); std::string line; std::getline(f,line); int n=0; double sum=0;
while(std::getline(f,line)){ std::stringstream ss(line); std::string field; int col=0; while(std::getline(ss,field,',')){ if(col==14) sum += std::stod(field); col++; } n++; }
std::ofstream out("../outputs/cpp_narrative_identity_summary.txt"); out<<"n="<<n<<"\nnarrative_integration_mean="<<sum/n<<"\n"; std::cout<<"Wrote C++ output.\n"; }
