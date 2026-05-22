use std::{collections::HashMap, fs, path::Path};
fn main() {
    let root = Path::new("..");
    let content = fs::read_to_string(root.join("data/synthetic_personality_twin_data.csv")).unwrap();
    let mut lines = content.lines();
    let header: Vec<&str> = lines.next().unwrap().split(',').collect();
    let zyg = header.iter().position(|h| *h == "zygosity").unwrap();
    let gxe = header.iter().position(|h| *h == "gxe_marker").unwrap();
    let mut counts: HashMap<String, usize> = HashMap::new();
    let mut sums: HashMap<String, f64> = HashMap::new();
    for line in lines {
        let f: Vec<&str> = line.split(',').collect();
        let k = f[zyg].to_string();
        let v: f64 = f[gxe].parse().unwrap();
        *counts.entry(k.clone()).or_insert(0) += 1;
        *sums.entry(k).or_insert(0.0) += v;
    }
    let out_dir = root.join("outputs"); fs::create_dir_all(&out_dir).unwrap();
    let mut out = String::from("zygosity,n,gxe_marker_mean\n");
    for (k, n) in counts { out.push_str(&format!("{},{},{:.4}\n", k, n, sums[&k] / n as f64)); }
    fs::write(out_dir.join("rust_gxe_by_zygosity.csv"), out).unwrap();
    println!("Wrote Rust output.");
}
