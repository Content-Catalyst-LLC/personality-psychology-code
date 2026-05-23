package main
import ("encoding/csv"; "fmt"; "log"; "os"; "path/filepath"; "strconv")
func main(){ root:=".."; f,err:=os.Open(filepath.Join(root,"data","synthetic_temperament_personality_longitudinal.csv")); if err!=nil{log.Fatal(err)}; defer f.Close()
r:=csv.NewReader(f); rec,err:=r.ReadAll(); if err!=nil{log.Fatal(err)}
h:=rec[0]; col:=func(n string) int { for i,v:= range h { if v==n { return i } }; log.Fatal("missing column: ", n); return -1 }
ctx:=col("developmental_context"); risk:=col("developmental_risk_index"); counts:=map[string]int{}; sums:=map[string]float64{}
for _,row:= range rec[1:] { v,_:=strconv.ParseFloat(row[risk],64); counts[row[ctx]]++; sums[row[ctx]]+=v }
outDir:=filepath.Join(root,"outputs"); os.MkdirAll(outDir,0755); out,_:=os.Create(filepath.Join(outDir,"go_risk_by_context.csv")); defer out.Close()
w:=csv.NewWriter(out); defer w.Flush(); w.Write([]string{"developmental_context","n","developmental_risk_mean"})
for k,n:= range counts { w.Write([]string{k, fmt.Sprintf("%d",n), fmt.Sprintf("%.4f",sums[k]/float64(n))}) }
fmt.Println("Wrote Go output.") }
