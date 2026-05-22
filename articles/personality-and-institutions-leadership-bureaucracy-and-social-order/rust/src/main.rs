use std::collections::HashMap;
use std::fs;
use std::path::Path;

fn main() {
    let root = Path::new("..");
    let data_path = root.join("data/synthetic_personality_institutions_bureaucracy.csv");
    let content = fs::read_to_string(&data_path).expect("could not read dataset");

    let mut lines = content.lines();
    let header: Vec<&str> = lines.next().expect("missing header").split(',').collect();

    let unit_idx = header.iter().position(|h| *h == "institutional_unit").expect("institutional_unit missing");
    let trust_idx = header.iter().position(|h| *h == "institutional_trust").expect("institutional_trust missing");

    let mut counts: HashMap<String, usize> = HashMap::new();
    let mut sums: HashMap<String, f64> = HashMap::new();

    for line in lines {
        let fields: Vec<&str> = line.split(',').collect();
        let unit = fields[unit_idx].to_string();
        let trust: f64 = fields[trust_idx].parse().expect("invalid trust value");

        *counts.entry(unit.clone()).or_insert(0) += 1;
        *sums.entry(unit).or_insert(0.0) += trust;
    }

    let out_dir = root.join("outputs");
    fs::create_dir_all(&out_dir).expect("could not create outputs");

    let mut output = String::from("institutional_unit,n,institutional_trust_mean\n");
    for (unit, n) in counts.iter() {
        let mean = sums[unit] / (*n as f64);
        output.push_str(&format!("{},{},{:.4}\n", unit, n, mean));
    }

    let out_path = out_dir.join("rust_institutional_trust_summary.csv");
    fs::write(&out_path, output).expect("could not write output");
    println!("Wrote Rust output: {}", out_path.display());
}
