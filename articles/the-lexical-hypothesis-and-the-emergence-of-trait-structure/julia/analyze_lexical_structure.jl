using DelimitedFiles, Statistics, Printf
root = normpath(joinpath(@__DIR__, ".."))
raw = readdlm(joinpath(root, "data", "synthetic_lexical_scores_for_sql.csv"), ',', String)
header = vec(raw[1, :]); rows = raw[2:end, :]
col(name) = findfirst(==(name), header)
metrics = ["sociable_cluster_score", "reliable_cluster_score", "compassionate_cluster_score", "anxious_cluster_score", "imaginative_cluster_score", "lexical_abundance_index", "structural_centrality_index", "cross_language_caution_index"]
mkpath(joinpath(root, "outputs"))
open(joinpath(root, "outputs", "julia_lexical_structure_summary.csv"), "w") do io
    println(io, "metric,mean,sd")
    for m in metrics
        vals = parse.(Float64, rows[:, col(m)])
        @printf(io, "%s,%.4f,%.4f\n", m, mean(vals), std(vals))
    end
end
println("Wrote Julia outputs.")
