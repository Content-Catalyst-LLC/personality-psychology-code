package main
import ("encoding/csv"; "fmt"; "log"; "os"; "path/filepath"; "strconv")
func main(){ root:=".."; f,err:=os.Open(filepath.Join(root,"data","synthetic_values_strivings_direction.csv")); if err!=nil{log.Fatal(err)}; defer f.Close()
r:=csv.NewReader(f); rec,err:=r.ReadAll(); if err!=nil{log.Fatal(err)}
h:=rec[0]; col:=func(n string) int { for i,v:= range h { if v==n { return i } }; log.Fatal("missing column: ", n); return -1 }
ctx:=col("value_context"); dir:=col("life_direction_coherence"); counts:=map[string]int{}; sums:=map[string]float64{}
for _,row:= range rec[1:] { v,_:=strconv.ParseFloat(row[dir],64); counts[row[ctx]]++; sums[row[ctx]]+=v }
outDir:=filepath.Join(root,"outputs"); os.MkdirAll(outDir,0755); out,_:=os.Create(filepath.Join(outDir,"go_life_direction_context_summary.csv")); defer out.Close()
w:=csv.NewWriter(out); defer w.Flush(); w.Write([]string{"value_context","n","life_direction_coherence_mean"})
for k,n:= range counts { w.Write([]string{k, fmt.Sprintf("%d",n), fmt.Sprintf("%.4f",sums[k]/float64(n))}) }
fmt.Println("Wrote Go output.") }
