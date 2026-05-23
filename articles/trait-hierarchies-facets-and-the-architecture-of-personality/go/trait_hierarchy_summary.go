package main
import ("encoding/csv"; "fmt"; "log"; "os"; "path/filepath"; "strconv")
func main(){ root:=".."; f,err:=os.Open(filepath.Join(root,"data","synthetic_hierarchical_trait_items.csv")); if err!=nil{log.Fatal(err)}; defer f.Close()
r:=csv.NewReader(f); rec,err:=r.ReadAll(); if err!=nil{log.Fatal(err)}
h:=rec[0]; col:=func(n string) int { for i,v:= range h { if v==n { return i } }; log.Fatal("missing column: ", n); return -1 }
disp:=col("facet_profile_dispersion"); cons:=col("hierarchy_consistency_index"); var n int; var sumD,sumC float64
for _,row:= range rec[1:] { d,_:=strconv.ParseFloat(row[disp],64); c,_:=strconv.ParseFloat(row[cons],64); sumD+=d; sumC+=c; n++ }
outDir:=filepath.Join(root,"outputs"); os.MkdirAll(outDir,0755); out,_:=os.Create(filepath.Join(outDir,"go_hierarchy_summary.csv")); defer out.Close()
w:=csv.NewWriter(out); defer w.Flush(); w.Write([]string{"n","facet_profile_dispersion_mean","hierarchy_consistency_mean"}); w.Write([]string{fmt.Sprintf("%d",n), fmt.Sprintf("%.4f",sumD/float64(n)), fmt.Sprintf("%.4f",sumC/float64(n))})
fmt.Println("Wrote Go output.") }
