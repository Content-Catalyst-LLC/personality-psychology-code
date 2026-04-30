# Toy personality organization update model.

personality = 0.50
trait_stability = 0.75
self_regulation = 0.70
maladaptive_pressure = 0.25
revision_rate = 0.08

for t in 1:12
    personality = personality + revision_rate * (0.35 * trait_stability + 0.35 * self_regulation - 0.30 * maladaptive_pressure)
    personality = clamp(personality, 0.0, 1.0)
    println("Time ", t, ": personality organization = ", round(personality, digits=3))
end
