use std::collections::HashMap;
use std::fs;
use std::path::Path;

fn main() {
    let root = Path::new("..");
    let data_path = root.join("data/synthetic_personality_culture_universality.csv");
    let content = fs::read_to_string(&data_path).expect("could not read dataset");

    let mut lines = content.lines();
    let header: Vec<&str> = lines.next().expect("missing header").split(',').collect();

    let group_idx = header.iter().position(|h| *h == "culture_group").expect("culture_group missing");
    let openness_idx = header.iter().position(|h| *h == "openness").expect("openness missing");

    let mut counts: HashMap<String, usize> = HashMap::new();
    let mut sums: HashMap<String, f64> = HashMap::new();

    for line in lines {
        let fields: Vec<&str> = line.split(',').collect();
        let group = fields[group_idx].to_string();
        let openness: f64 = fields[openness_idx].parse().expect("invalid openness value");

        *counts.entry(group.clone()).or_insert(0) += 1;
        *sums.entry(group).or_insert(0.0) += openness;
    }

    let out_dir = root.join("outputs");
    fs::create_dir_all(&out_dir).expect("could not create outputs");

    let mut output = String::from("culture_group,n,openness_mean\n");
    for (group, n) in counts.iter() {
        let mean = sums[group] / (*n as f64);
        output.push_str(&format!("{},{},{:.4}\n", group, n, mean));
    }

    let out_path = out_dir.join("rust_openness_summary.csv");
    fs::write(&out_path, output).expect("could not write output");
    println!("Wrote Rust output: {}", out_path.display());
}
