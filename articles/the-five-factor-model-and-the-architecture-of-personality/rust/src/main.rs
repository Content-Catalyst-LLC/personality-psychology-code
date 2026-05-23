use std::{fs, path::Path};
fn main() {
    let root = Path::new("..");
    let content = fs::read_to_string(root.join("data/synthetic_ffm_scores_for_sql.csv")).unwrap();
    let mut lines = content.lines();
    let header: Vec<&str> = lines.next().unwrap().split(',').collect();
    let consistency = header.iter().position(|h| *h == "hierarchy_consistency_index").unwrap();
    let mut n = 0usize;
    let mut sum = 0.0f64;
    for line in lines {
        let f: Vec<&str> = line.split(',').collect();
        sum += f[consistency].parse::<f64>().unwrap();
        n += 1;
    }
    let out_dir = root.join("outputs"); fs::create_dir_all(&out_dir).unwrap();
    fs::write(out_dir.join("rust_hierarchy_consistency_summary.csv"), format!("n,hierarchy_consistency_index_mean\n{},{:.4}\n", n, sum / n as f64)).unwrap();
    println!("Wrote Rust output.");
}
