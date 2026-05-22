package main

import (
	"encoding/csv"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"strconv"
)

func mustFloat(value string) float64 {
	parsed, err := strconv.ParseFloat(value, 64)
	if err != nil {
		log.Fatalf("could not parse float %q: %v", value, err)
	}
	return parsed
}

func main() {
	dataPath := filepath.Join("data", "synthetic_personality_creativity.csv")
	file, err := os.Open(dataPath)
	if err != nil {
		log.Fatalf("could not open %s: %v", dataPath, err)
	}
	defer file.Close()

	reader := csv.NewReader(file)
	records, err := reader.ReadAll()
	if err != nil {
		log.Fatalf("could not read CSV: %v", err)
	}

	if len(records) < 2 {
		log.Fatal("dataset has no data rows")
	}

	headers := records[0]
	index := make(map[string]int)
	for i, header := range headers {
		index[header] = i
	}

	var n float64
	var opennessSum float64
	var divergentSum float64
	var achievementSum float64

	for _, row := range records[1:] {
		n++
		opennessSum += mustFloat(row[index["openness"]])
		divergentSum += mustFloat(row[index["divergent_thinking"]])
		achievementSum += mustFloat(row[index["creative_achievement"]])
	}

	fmt.Printf("Rows: %.0f\n", n)
	fmt.Printf("Mean openness: %.2f\n", opennessSum/n)
	fmt.Printf("Mean divergent thinking: %.2f\n", divergentSum/n)
	fmt.Printf("Mean creative achievement: %.2f\n", achievementSum/n)
}
