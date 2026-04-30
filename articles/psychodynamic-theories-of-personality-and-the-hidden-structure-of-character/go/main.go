package main

import "fmt"

func personalityOrganization(trait, motive, identity, regulation, adaptation, pressure float64) float64 {
	return 0.18*trait + 0.16*motive + 0.18*identity + 0.18*regulation + 0.14*adaptation - 0.20*pressure
}

func main() {
	score := personalityOrganization(0.78, 0.72, 0.68, 0.74, 0.63, 0.22)
	fmt.Printf("Personality organization score: %.3f\n", score)
}
