package main
import ("encoding/csv"; "fmt"; "log"; "os"; "path/filepath"; "strconv")
func main(){ root:=".."; f,err:=os.Open(filepath.Join(root,"data","synthetic_alternative_structure_scores_for_sql.csv")); if err!=nil{log.Fatal(err)}; defer f.Close()
r:=csv.NewReader(f); rec,err:=r.ReadAll(); if err!=nil{log.Fatal(err)}
h:=rec[0]; col:=func(n string) int { for i,v:= range h { if v==n { return i } }; log.Fatal("missing column: ", n); return -1 }
inc:=col("hexaco_increment_marker"); gap:=col("repartitioning_gap"); var n int; var sumI,sumG float64
for _,row:= range rec[1:] { i,_:=strconv.ParseFloat(row[inc],64); g,_:=strconv.ParseFloat(row[gap],64); sumI+=i; sumG+=g; n++ }
outDir:=filepath.Join(root,"outputs"); os.MkdirAll(outDir,0755); out,_:=os.Create(filepath.Join(outDir,"go_alternative_structure_summary.csv")); defer out.Close()
w:=csv.NewWriter(out); defer w.Flush(); w.Write([]string{"n","hexaco_increment_marker_mean","repartitioning_gap_mean"}); w.Write([]string{fmt.Sprintf("%d",n), fmt.Sprintf("%.4f",sumI/float64(n)), fmt.Sprintf("%.4f",sumG/float64(n))})
fmt.Println("Wrote Go output.") }
