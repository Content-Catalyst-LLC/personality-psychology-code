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
	dataPath := filepath.Join(root, "data", "synthetic_personality_work_leadership.csv")
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

	roleIdx := col("role_family")
	performanceIdx := col("job_performance")

	counts := map[string]int{}
	sums := map[string]float64{}

	for _, row := range records[1:] {
		role := row[roleIdx]
		value, err := strconv.ParseFloat(row[performanceIdx], 64)
		if err != nil {
			log.Fatal(err)
		}
		counts[role]++
		sums[role] += value
	}

	outDir := filepath.Join(root, "outputs")
	os.MkdirAll(outDir, 0755)
	outPath := filepath.Join(outDir, "go_job_performance_summary.csv")
	out, err := os.Create(outPath)
	if err != nil {
		log.Fatal(err)
	}
	defer out.Close()

	writer := csv.NewWriter(out)
	defer writer.Flush()

	writer.Write([]string{"role_family", "n", "job_performance_mean"})
	for role, n := range counts {
		writer.Write([]string{role, fmt.Sprintf("%d", n), fmt.Sprintf("%.4f", sums[role]/float64(n))})
	}

	fmt.Println("Wrote Go output:", outPath)
}
