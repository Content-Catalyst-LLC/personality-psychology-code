package main
import ("encoding/csv"; "fmt"; "log"; "os"; "path/filepath"; "strconv")
func main(){ root:=".."; f,err:=os.Open(filepath.Join(root,"data","synthetic_lexical_scores_for_sql.csv")); if err!=nil{log.Fatal(err)}; defer f.Close()
r:=csv.NewReader(f); rec,err:=r.ReadAll(); if err!=nil{log.Fatal(err)}
h:=rec[0]; col:=func(n string) int { for i,v:= range h { if v==n { return i } }; log.Fatal("missing column: ", n); return -1 }
central:=col("structural_centrality_index"); caution:=col("cross_language_caution_index"); var n int; var sumC,sumL float64
for _,row:= range rec[1:] { c,_:=strconv.ParseFloat(row[central],64); l,_:=strconv.ParseFloat(row[caution],64); sumC+=c; sumL+=l; n++ }
outDir:=filepath.Join(root,"outputs"); os.MkdirAll(outDir,0755); out,_:=os.Create(filepath.Join(outDir,"go_lexical_summary.csv")); defer out.Close()
w:=csv.NewWriter(out); defer w.Flush(); w.Write([]string{"n","structural_centrality_index_mean","cross_language_caution_index_mean"}); w.Write([]string{fmt.Sprintf("%d",n), fmt.Sprintf("%.4f",sumC/float64(n)), fmt.Sprintf("%.4f",sumL/float64(n))})
fmt.Println("Wrote Go output.") }
