using DelimitedFiles, Statistics, Printf
root = normpath(joinpath(@__DIR__, ".."))
raw = readdlm(joinpath(root, "data", "synthetic_personality_summary_for_sql.csv"), ',', String)
header = vec(raw[1, :]); rows = raw[2:end, :]
col(name) = findfirst(==(name), header)
metrics = ["conscientiousness_score", "extraversion_score", "neuroticism_score", "identity_coherence", "life_satisfaction", "responsible_interpretation_index"]
mkpath(joinpath(root, "outputs"))
open(joinpath(root, "outputs", "julia_personality_psychology_summary.csv"), "w") do io
    println(io, "metric,mean,sd")
    for m in metrics
        vals = parse.(Float64, rows[:, col(m)])
        @printf(io, "%s,%.4f,%.4f\n", m, mean(vals), std(vals))
    end
end
println("Wrote Julia outputs.")
