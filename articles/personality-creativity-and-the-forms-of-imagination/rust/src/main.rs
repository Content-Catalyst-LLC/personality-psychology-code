use std::fs;
use std::path::Path;

fn main() {
    let path = Path::new("../data/synthetic_personality_creativity.csv");
    let text = fs::read_to_string(path).expect("could not read synthetic data");
    let mut lines = text.lines();
    let headers: Vec<&str> = lines.next().expect("missing header").split(',').collect();
    let openness_idx = headers.iter().position(|h| *h == "openness").unwrap();
    let achievement_idx = headers.iter().position(|h| *h == "creative_achievement").unwrap();

    let mut n = 0.0;
    let mut openness_sum = 0.0;
    let mut achievement_sum = 0.0;

    for line in lines {
        let fields: Vec<&str> = line.split(',').collect();
        openness_sum += fields[openness_idx].parse::<f64>().unwrap();
        achievement_sum += fields[achievement_idx].parse::<f64>().unwrap();
        n += 1.0;
    }

    println!("Rust summary utility");
    println!("mean openness: {:.2}", openness_sum / n);
    println!("mean creative achievement: {:.2}", achievement_sum / n);
}
