using DelimitedFiles, Statistics, Printf
root = normpath(joinpath(@__DIR__, ".."))
raw = readdlm(joinpath(root, "data", "synthetic_self_concept_self_esteem_self_knowledge.csv"), ',', String)
header = vec(raw[1, :]); rows = raw[2:end, :]
col(name) = findfirst(==(name), header)
contexts = unique(rows[:, col("self_system_context")])
metrics = ["self_concept_positivity", "self_esteem", "self_knowledge_accuracy", "total_self_discrepancy", "social_recognition", "external_devaluation", "well_being"]
mkpath(joinpath(root, "outputs"))
open(joinpath(root, "outputs", "julia_self_system_context_summary.csv"), "w") do io
    println(io, "self_system_context,n," * join([m * "_mean" for m in metrics], ","))
    for c in contexts
        sub = rows[rows[:, col("self_system_context")] .== c, :]
        vals = [mean(parse.(Float64, sub[:, col(m)])) for m in metrics]
        @printf(io, "%s,%d,%s\n", c, size(sub, 1), join(round.(vals, digits=4), ","))
    end
end
println("Wrote Julia outputs.")
