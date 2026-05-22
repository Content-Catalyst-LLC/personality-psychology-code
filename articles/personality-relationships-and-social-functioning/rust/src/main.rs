use std::collections::HashMap;
use std::fs;
use std::path::Path;

fn main() {
    let root = Path::new("..");
    let data_path = root.join("data/synthetic_personality_relationships_social_functioning.csv");
    let content = fs::read_to_string(&data_path).expect("could not read dataset");

    let mut lines = content.lines();
    let header: Vec<&str> = lines.next().expect("missing header").split(',').collect();

    let context_idx = header.iter().position(|h| *h == "social_context").expect("social_context missing");
    let satisfaction_idx = header.iter().position(|h| *h == "relationship_satisfaction").expect("relationship_satisfaction missing");

    let mut counts: HashMap<String, usize> = HashMap::new();
    let mut sums: HashMap<String, f64> = HashMap::new();

    for line in lines {
        let fields: Vec<&str> = line.split(',').collect();
        let context = fields[context_idx].to_string();
        let satisfaction: f64 = fields[satisfaction_idx].parse().expect("invalid satisfaction value");

        *counts.entry(context.clone()).or_insert(0) += 1;
        *sums.entry(context).or_insert(0.0) += satisfaction;
    }

    let out_dir = root.join("outputs");
    fs::create_dir_all(&out_dir).expect("could not create outputs");

    let mut output = String::from("social_context,n,relationship_satisfaction_mean\n");
    for (context, n) in counts.iter() {
        let mean = sums[context] / (*n as f64);
        output.push_str(&format!("{},{},{:.4}\n", context, n, mean));
    }

    let out_path = out_dir.join("rust_relationship_satisfaction_summary.csv");
    fs::write(&out_path, output).expect("could not write output");
    println!("Wrote Rust output: {}", out_path.display());
}
