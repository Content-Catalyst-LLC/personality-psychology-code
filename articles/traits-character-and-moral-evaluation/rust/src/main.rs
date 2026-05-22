use std::{collections::HashMap, fs, path::Path};
fn main() {
    let root = Path::new("..");
    let content = fs::read_to_string(root.join("data/synthetic_traits_character_morality.csv")).unwrap();
    let mut lines = content.lines();
    let header: Vec<&str> = lines.next().unwrap().split(',').collect();
    let ctx = header.iter().position(|h| *h == "evaluation_context").unwrap();
    let ch = header.iter().position(|h| *h == "moral_character_index").unwrap();
    let mut counts: HashMap<String, usize> = HashMap::new();
    let mut sums: HashMap<String, f64> = HashMap::new();
    for line in lines {
        let f: Vec<&str> = line.split(',').collect();
        let k = f[ctx].to_string();
        let v: f64 = f[ch].parse().unwrap();
        *counts.entry(k.clone()).or_insert(0) += 1;
        *sums.entry(k).or_insert(0.0) += v;
    }
    let out_dir = root.join("outputs"); fs::create_dir_all(&out_dir).unwrap();
    let mut out = String::from("evaluation_context,n,moral_character_index_mean\n");
    for (k, n) in counts { out.push_str(&format!("{},{},{:.4}\n", k, n, sums[&k] / n as f64)); }
    fs::write(out_dir.join("rust_moral_character_summary.csv"), out).unwrap();
    println!("Wrote Rust output.");
}
