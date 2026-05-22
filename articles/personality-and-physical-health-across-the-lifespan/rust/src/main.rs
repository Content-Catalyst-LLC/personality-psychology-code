use std::collections::HashMap;
use std::fs;
use std::path::Path;

fn main() {
    let root = Path::new("..");
    let data_path = root.join("data/synthetic_personality_physical_health_lifespan.csv");
    let content = fs::read_to_string(&data_path).expect("could not read dataset");

    let mut lines = content.lines();
    let header: Vec<&str> = lines.next().expect("missing header").split(',').collect();

    let age_band_idx = header.iter().position(|h| *h == "age_band").expect("age_band missing");
    let health_idx = header.iter().position(|h| *h == "physical_health_score").expect("physical_health_score missing");

    let mut counts: HashMap<String, usize> = HashMap::new();
    let mut sums: HashMap<String, f64> = HashMap::new();

    for line in lines {
        let fields: Vec<&str> = line.split(',').collect();
        let age_band = fields[age_band_idx].to_string();
        let health: f64 = fields[health_idx].parse().expect("invalid health value");

        *counts.entry(age_band.clone()).or_insert(0) += 1;
        *sums.entry(age_band).or_insert(0.0) += health;
    }

    let out_dir = root.join("outputs");
    fs::create_dir_all(&out_dir).expect("could not create outputs");

    let mut output = String::from("age_band,n,physical_health_score_mean\n");
    for (age_band, n) in counts.iter() {
        let mean = sums[age_band] / (*n as f64);
        output.push_str(&format!("{},{},{:.4}\n", age_band, n, mean));
    }

    let out_path = out_dir.join("rust_physical_health_summary.csv");
    fs::write(&out_path, output).expect("could not write output");
    println!("Wrote Rust output: {}", out_path.display());
}
