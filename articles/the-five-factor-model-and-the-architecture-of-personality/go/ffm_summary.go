package main
import ("encoding/csv"; "fmt"; "log"; "os"; "path/filepath"; "strconv")
func main(){ root:=".."; f,err:=os.Open(filepath.Join(root,"data","synthetic_ffm_scores_for_sql.csv")); if err!=nil{log.Fatal(err)}; defer f.Close()
r:=csv.NewReader(f); rec,err:=r.ReadAll(); if err!=nil{log.Fatal(err)}
h:=rec[0]; col:=func(n string) int { for i,v:= range h { if v==n { return i } }; log.Fatal("missing column: ", n); return -1 }
align:=col("domain_facet_alignment"); gap:=col("bandwidth_fidelity_gap"); var n int; var sumA,sumG float64
for _,row:= range rec[1:] { a,_:=strconv.ParseFloat(row[align],64); g,_:=strconv.ParseFloat(row[gap],64); sumA+=a; sumG+=g; n++ }
outDir:=filepath.Join(root,"outputs"); os.MkdirAll(outDir,0755); out,_:=os.Create(filepath.Join(outDir,"go_ffm_summary.csv")); defer out.Close()
w:=csv.NewWriter(out); defer w.Flush(); w.Write([]string{"n","domain_facet_alignment_mean","bandwidth_fidelity_gap_mean"}); w.Write([]string{fmt.Sprintf("%d",n), fmt.Sprintf("%.4f",sumA/float64(n)), fmt.Sprintf("%.4f",sumG/float64(n))})
fmt.Println("Wrote Go output.") }
