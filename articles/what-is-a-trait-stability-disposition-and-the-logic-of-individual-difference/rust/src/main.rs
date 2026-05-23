use std::{fs, path::Path};
fn main() {
    let root = Path::new("..");
    let content = fs::read_to_string(root.join("data/synthetic_trait_state_summary_for_sql.csv")).unwrap();
    let mut lines = content.lines();
    let header: Vec<&str> = lines.next().unwrap().split(',').collect();
    let agg = header.iter().position(|h| *h == "aggregation_reliability_index").unwrap();
    let mut n = 0usize;
    let mut sum = 0.0f64;
    for line in lines {
        let f: Vec<&str> = line.split(',').collect();
        sum += f[agg].parse::<f64>().unwrap();
        n += 1;
    }
    let out_dir = root.join("outputs"); fs::create_dir_all(&out_dir).unwrap();
    fs::write(out_dir.join("rust_aggregation_reliability_summary.csv"), format!("n,aggregation_reliability_index_mean\n{},{:.4}\n", n, sum / n as f64)).unwrap();
    println!("Wrote Rust output.");
}
