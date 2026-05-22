use std::{collections::HashMap, fs, path::Path};
fn main() {
    let root = Path::new("..");
    let content = fs::read_to_string(root.join("data/synthetic_selfhood_agency_identity.csv")).unwrap();
    let mut lines = content.lines();
    let header: Vec<&str> = lines.next().unwrap().split(',').collect();
    let ctx = header.iter().position(|h| *h == "identity_context").unwrap();
    let agency = header.iter().position(|h| *h == "situated_agency_index").unwrap();
    let mut counts: HashMap<String, usize> = HashMap::new();
    let mut sums: HashMap<String, f64> = HashMap::new();
    for line in lines {
        let f: Vec<&str> = line.split(',').collect();
        let k = f[ctx].to_string();
        let v: f64 = f[agency].parse().unwrap();
        *counts.entry(k.clone()).or_insert(0) += 1;
        *sums.entry(k).or_insert(0.0) += v;
    }
    let out_dir = root.join("outputs"); fs::create_dir_all(&out_dir).unwrap();
    let mut out = String::from("identity_context,n,situated_agency_mean\n");
    for (k, n) in counts { out.push_str(&format!("{},{},{:.4}\n", k, n, sums[&k] / n as f64)); }
    fs::write(out_dir.join("rust_situated_agency_context_summary.csv"), out).unwrap();
    println!("Wrote Rust output.");
}
