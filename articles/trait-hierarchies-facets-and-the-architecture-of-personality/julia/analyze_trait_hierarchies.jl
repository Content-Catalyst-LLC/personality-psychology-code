using DelimitedFiles, Statistics, Printf
root = normpath(joinpath(@__DIR__, ".."))
raw = readdlm(joinpath(root, "data", "synthetic_hierarchical_trait_items.csv"), ',', String)
header = vec(raw[1, :]); rows = raw[2:end, :]
col(name) = findfirst(==(name), header)
metrics = ["extraversion_score", "agreeableness_score", "conscientiousness_score", "neuroticism_score", "openness_score", "facet_profile_dispersion", "hierarchy_consistency_index"]
mkpath(joinpath(root, "outputs"))
open(joinpath(root, "outputs", "julia_trait_hierarchy_summary.csv"), "w") do io
    println(io, "metric,mean,sd")
    for m in metrics
        vals = parse.(Float64, rows[:, col(m)])
        @printf(io, "%s,%.4f,%.4f\n", m, mean(vals), std(vals))
    end
end
println("Wrote Julia outputs.")
