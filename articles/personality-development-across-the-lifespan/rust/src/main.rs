fn personality_organization(trait: f64, motive: f64, identity: f64, regulation: f64, adaptation: f64, pressure: f64) -> f64 {
    0.18 * trait + 0.16 * motive + 0.18 * identity + 0.18 * regulation + 0.14 * adaptation - 0.20 * pressure
}

fn main() {
    let score = personality_organization(0.78, 0.72, 0.68, 0.74, 0.63, 0.22);
    println!("Personality organization score: {:.3}", score);
}
