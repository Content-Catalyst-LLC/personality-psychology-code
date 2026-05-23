package main
import ("encoding/csv"; "fmt"; "log"; "os"; "path/filepath"; "strconv")
func main(){ root:=".."; f,err:=os.Open(filepath.Join(root,"data","synthetic_personality_summary_for_sql.csv")); if err!=nil{log.Fatal(err)}; defer f.Close()
r:=csv.NewReader(f); rec,err:=r.ReadAll(); if err!=nil{log.Fatal(err)}
h:=rec[0]; col:=func(n string) int { for i,v:= range h { if v==n { return i } }; log.Fatal("missing column: ", n); return -1 }
identity:=col("identity_coherence"); interp:=col("responsible_interpretation_index"); var n int; var sumI,sumR float64
for _,row:= range rec[1:] { i,_:=strconv.ParseFloat(row[identity],64); r,_:=strconv.ParseFloat(row[interp],64); sumI+=i; sumR+=r; n++ }
outDir:=filepath.Join(root,"outputs"); os.MkdirAll(outDir,0755); out,_:=os.Create(filepath.Join(outDir,"go_personality_psychology_summary.csv")); defer out.Close()
w:=csv.NewWriter(out); defer w.Flush(); w.Write([]string{"n","identity_coherence_mean","responsible_interpretation_index_mean"}); w.Write([]string{fmt.Sprintf("%d",n), fmt.Sprintf("%.4f",sumI/float64(n)), fmt.Sprintf("%.4f",sumR/float64(n))})
fmt.Println("Wrote Go output.") }
