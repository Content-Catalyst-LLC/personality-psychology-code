use std::{collections::HashMap, fs, path::Path};
fn main() {
    let root = Path::new("..");
    let content = fs::read_to_string(root.join("data/synthetic_types_traits_dimensional_models.csv")).unwrap();
    let mut lines = content.lines();
    let header: Vec<&str> = lines.next().unwrap().split(',').collect();
    let profile_col = header.iter().position(|h| *h == "profile_type").unwrap();
    let mut counts: HashMap<String, usize> = HashMap::new();
    for line in lines {
        let f: Vec<&str> = line.split(',').collect();
        *counts.entry(f[profile_col].to_string()).or_insert(0) += 1;
    }
    let out_dir = root.join("outputs"); fs::create_dir_all(&out_dir).unwrap();
    let mut out = String::from("profile_type,n\n");
    for (k, n) in counts { out.push_str(&format!("{},{}\n", k, n)); }
    fs::write(out_dir.join("rust_profile_type_counts.csv"), out).unwrap();
    println!("Wrote Rust output.");
}
