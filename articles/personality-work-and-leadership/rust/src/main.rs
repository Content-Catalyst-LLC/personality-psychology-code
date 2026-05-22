use std::collections::HashMap;
use std::fs;
use std::path::Path;

fn main() {
    let root = Path::new("..");
    let data_path = root.join("data/synthetic_personality_work_leadership.csv");
    let content = fs::read_to_string(&data_path).expect("could not read dataset");

    let mut lines = content.lines();
    let header: Vec<&str> = lines.next().expect("missing header").split(',').collect();

    let role_idx = header.iter().position(|h| *h == "role_family").expect("role_family missing");
    let performance_idx = header.iter().position(|h| *h == "job_performance").expect("job_performance missing");

    let mut counts: HashMap<String, usize> = HashMap::new();
    let mut sums: HashMap<String, f64> = HashMap::new();

    for line in lines {
        let fields: Vec<&str> = line.split(',').collect();
        let role = fields[role_idx].to_string();
        let performance: f64 = fields[performance_idx].parse().expect("invalid performance value");

        *counts.entry(role.clone()).or_insert(0) += 1;
        *sums.entry(role).or_insert(0.0) += performance;
    }

    let out_dir = root.join("outputs");
    fs::create_dir_all(&out_dir).expect("could not create outputs");

    let mut output = String::from("role_family,n,job_performance_mean\n");
    for (role, n) in counts.iter() {
        let mean = sums[role] / (*n as f64);
        output.push_str(&format!("{},{},{:.4}\n", role, n, mean));
    }

    let out_path = out_dir.join("rust_job_performance_summary.csv");
    fs::write(&out_path, output).expect("could not write output");
    println!("Wrote Rust output: {}", out_path.display());
}
