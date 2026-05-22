use std::error::Error;

fn main() -> Result<(), Box<dyn Error>> {
    let mut reader = csv::Reader::from_path("../data/synthetic_personality_creativity.csv")
        .or_else(|_| csv::Reader::from_path("data/synthetic_personality_creativity.csv"))?;

    let headers = reader.headers()?.clone();

    let openness_idx = headers.iter().position(|h| h == "openness").unwrap();
    let divergent_idx = headers.iter().position(|h| h == "divergent_thinking").unwrap();
    let achievement_idx = headers.iter().position(|h| h == "creative_achievement").unwrap();

    let mut n = 0.0;
    let mut openness_sum = 0.0;
    let mut divergent_sum = 0.0;
    let mut achievement_sum = 0.0;

    for result in reader.records() {
        let record = result?;
        n += 1.0;
        openness_sum += record[openness_idx].parse::<f64>()?;
        divergent_sum += record[divergent_idx].parse::<f64>()?;
        achievement_sum += record[achievement_idx].parse::<f64>()?;
    }

    println!("Rows: {}", n as i64);
    println!("Mean openness: {:.2}", openness_sum / n);
    println!("Mean divergent thinking: {:.2}", divergent_sum / n);
    println!("Mean creative achievement: {:.2}", achievement_sum / n);

    Ok(())
}
