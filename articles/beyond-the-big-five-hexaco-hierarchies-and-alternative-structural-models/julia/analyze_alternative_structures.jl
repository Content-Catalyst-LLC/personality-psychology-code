using DelimitedFiles, Statistics, Printf
root = normpath(joinpath(@__DIR__, ".."))
raw = readdlm(joinpath(root, "data", "synthetic_alternative_structure_scores_for_sql.csv"), ',', String)
header = vec(raw[1, :]); rows = raw[2:end, :]
col(name) = findfirst(==(name), header)
metrics = ["bf_agreeableness", "hx_honesty_humility", "hx_agreeableness", "hx_emotionality", "outcome_integrity", "outcome_exploitative_risk", "hexaco_increment_marker", "repartitioning_gap"]
mkpath(joinpath(root, "outputs"))
open(joinpath(root, "outputs", "julia_alternative_structure_summary.csv"), "w") do io
    println(io, "metric,mean,sd")
    for m in metrics
        vals = parse.(Float64, rows[:, col(m)])
        @printf(io, "%s,%.4f,%.4f\n", m, mean(vals), std(vals))
    end
end
println("Wrote Julia outputs.")
