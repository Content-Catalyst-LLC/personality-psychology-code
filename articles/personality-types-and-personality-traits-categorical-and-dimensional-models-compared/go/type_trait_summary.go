package main
import ("encoding/csv"; "fmt"; "log"; "os"; "path/filepath")
func main(){ root:=".."; f,err:=os.Open(filepath.Join(root,"data","synthetic_types_traits_dimensional_models.csv")); if err!=nil{log.Fatal(err)}; defer f.Close()
r:=csv.NewReader(f); rec,err:=r.ReadAll(); if err!=nil{log.Fatal(err)}
h:=rec[0]; col:=func(n string) int { for i,v:= range h { if v==n { return i } }; log.Fatal("missing column: ", n); return -1 }
profileCol:=col("profile_type"); counts:=map[string]int{}
for _,row:= range rec[1:] { counts[row[profileCol]]++ }
outDir:=filepath.Join(root,"outputs"); os.MkdirAll(outDir,0755); out,_:=os.Create(filepath.Join(outDir,"go_profile_type_counts.csv")); defer out.Close()
w:=csv.NewWriter(out); defer w.Flush(); w.Write([]string{"profile_type","n"})
for k,n:= range counts { w.Write([]string{k, fmt.Sprintf("%d",n)}) }
fmt.Println("Wrote Go output.") }
