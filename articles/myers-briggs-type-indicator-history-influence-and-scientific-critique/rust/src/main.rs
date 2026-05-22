use std::{collections::HashMap, fs, path::Path};
fn main() {
    let root = Path::new("..");
    let content = fs::read_to_string(root.join("data/synthetic_mbti_typology_vs_traits.csv")).unwrap();
    let mut lines = content.lines();
    let header: Vec<&str> = lines.next().unwrap().split(',').collect();
    let type_col = header.iter().position(|h| *h == "type_code").unwrap();
    let mut counts: HashMap<String, usize> = HashMap::new();
    for line in lines {
        let f: Vec<&str> = line.split(',').collect();
        *counts.entry(f[type_col].to_string()).or_insert(0) += 1;
    }
    let out_dir = root.join("outputs"); fs::create_dir_all(&out_dir).unwrap();
    let mut out = String::from("type_code,n\n");
    for (k, n) in counts { out.push_str(&format!("{},{}\n", k, n)); }
    fs::write(out_dir.join("rust_mbti_type_frequencies.csv"), out).unwrap();
    println!("Wrote Rust output.");
}
