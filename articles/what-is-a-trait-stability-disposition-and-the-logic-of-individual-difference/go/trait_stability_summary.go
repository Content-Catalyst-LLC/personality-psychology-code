package main
import ("encoding/csv"; "fmt"; "log"; "os"; "path/filepath"; "strconv")
func main(){ root:=".."; f,err:=os.Open(filepath.Join(root,"data","synthetic_trait_state_summary_for_sql.csv")); if err!=nil{log.Fatal(err)}; defer f.Close()
r:=csv.NewReader(f); rec,err:=r.ReadAll(); if err!=nil{log.Fatal(err)}
h:=rec[0]; col:=func(n string) int { for i,v:= range h { if v==n { return i } }; log.Fatal("missing column: ", n); return -1 }
align:=col("trait_state_alignment_index"); variability:=col("state_variability_index"); var n int; var sumA,sumV float64
for _,row:= range rec[1:] { a,_:=strconv.ParseFloat(row[align],64); v,_:=strconv.ParseFloat(row[variability],64); sumA+=a; sumV+=v; n++ }
outDir:=filepath.Join(root,"outputs"); os.MkdirAll(outDir,0755); out,_:=os.Create(filepath.Join(outDir,"go_trait_stability_summary.csv")); defer out.Close()
w:=csv.NewWriter(out); defer w.Flush(); w.Write([]string{"n","trait_state_alignment_index_mean","state_variability_index_mean"}); w.Write([]string{fmt.Sprintf("%d",n), fmt.Sprintf("%.4f",sumA/float64(n)), fmt.Sprintf("%.4f",sumV/float64(n))})
fmt.Println("Wrote Go output.") }
