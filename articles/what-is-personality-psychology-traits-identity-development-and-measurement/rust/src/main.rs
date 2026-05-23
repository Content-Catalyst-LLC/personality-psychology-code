use std::{fs, path::Path};
fn main() {
    let root = Path::new("..");
    let content = fs::read_to_string(root.join("data/synthetic_personality_summary_for_sql.csv")).unwrap();
    let mut lines = content.lines();
    let header: Vec<&str> = lines.next().unwrap().split(',').collect();
    let life = header.iter().position(|h| *h == "life_satisfaction").unwrap();
    let mut n = 0usize;
    let mut sum = 0.0f64;
    for line in lines {
        let f: Vec<&str> = line.split(',').collect();
        sum += f[life].parse::<f64>().unwrap();
        n += 1;
    }
    let out_dir = root.join("outputs"); fs::create_dir_all(&out_dir).unwrap();
    fs::write(out_dir.join("rust_life_satisfaction_summary.csv"), format!("n,life_satisfaction_mean\n{},{:.4}\n", n, sum / n as f64)).unwrap();
    println!("Wrote Rust output.");
}
