package main

import (
	"encoding/csv"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"strconv"
)

func main() {
	root := filepath.Join("..")
	path := filepath.Join(root, "data", "synthetic_personality_creativity.csv")
	file, err := os.Open(path)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	reader := csv.NewReader(file)
	records, err := reader.ReadAll()
	if err != nil {
		log.Fatal(err)
	}

	if len(records) < 2 {
		log.Fatal("no data rows found")
	}

	headers := records[0]
	idx := map[string]int{}
	for i, h := range headers {
		idx[h] = i
	}

	cols := []string{"openness", "intellect", "persistence", "social_support", "divergent_thinking", "creative_achievement", "everyday_creativity"}
	fmt.Println("Column means from Go summary utility")
	for _, col := range cols {
		sum := 0.0
		count := 0.0
		for _, row := range records[1:] {
			value, err := strconv.ParseFloat(row[idx[col]], 64)
			if err == nil {
				sum += value
				count++
			}
		}
		fmt.Printf("%s: %.2f\n", col, sum/count)
	}
}
