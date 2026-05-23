using DelimitedFiles, Statistics, Printf
root = normpath(joinpath(@__DIR__, ".."))
raw = readdlm(joinpath(root, "data", "synthetic_personality_history_scores_for_sql.csv"), ',', String)
header = vec(raw[1, :]); rows = raw[2:end, :]
col(name) = findfirst(==(name), header)
metrics = ["characterology_typology_index", "psychometric_structure_index", "person_situation_index", "narrative_identity_index", "measurement_invariance_caution_index", "historical_method_maturity_index"]
mkpath(joinpath(root, "outputs"))
open(joinpath(root, "outputs", "julia_personality_history_summary.csv"), "w") do io
    println(io, "metric,mean,sd")
    for m in metrics
        vals = parse.(Float64, rows[:, col(m)])
        @printf(io, "%s,%.4f,%.4f\n", m, mean(vals), std(vals))
    end
end
println("Wrote Julia outputs.")
