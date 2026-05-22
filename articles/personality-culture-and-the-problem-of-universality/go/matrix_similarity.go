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
	dataPath := filepath.Join(root, "data", "synthetic_personality_culture_universality.csv")
	file, err := os.Open(dataPath)
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
		log.Fatal("dataset has no rows")
	}

	header := records[0]
	col := func(name string) int {
		for i, h := range header {
			if h == name {
				return i
			}
		}
		log.Fatalf("missing column: %s", name)
		return -1
	}

	groupIdx := col("culture_group")
	openIdx := col("openness")

	counts := map[string]int{}
	sums := map[string]float64{}

	for _, row := range records[1:] {
		group := row[groupIdx]
		value, err := strconv.ParseFloat(row[openIdx], 64)
		if err != nil {
			log.Fatal(err)
		}
		counts[group]++
		sums[group] += value
	}

	outDir := filepath.Join(root, "outputs")
	os.MkdirAll(outDir, 0755)
	outPath := filepath.Join(outDir, "go_openness_summary.csv")
	out, err := os.Create(outPath)
	if err != nil {
		log.Fatal(err)
	}
	defer out.Close()

	writer := csv.NewWriter(out)
	defer writer.Flush()

	writer.Write([]string{"culture_group", "n", "openness_mean"})
	for group, n := range counts {
		writer.Write([]string{group, fmt.Sprintf("%d", n), fmt.Sprintf("%.4f", sums[group]/float64(n))})
	}

	fmt.Println("Wrote Go output:", outPath)
}
