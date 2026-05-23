using DelimitedFiles, Statistics, Printf
root = normpath(joinpath(@__DIR__, ".."))
raw = readdlm(joinpath(root, "data", "synthetic_temperament_personality_longitudinal.csv"), ',', String)
header = vec(raw[1, :]); rows = raw[2:end, :]
col(name) = findfirst(==(name), header)
contexts = unique(rows[:, col("developmental_context")])
metrics = ["inhibition_t1", "negative_affect_t1", "effortful_control_t1", "parenting_support_t1", "family_stress_t1", "developmental_risk_index", "adaptive_pathway_score"]
mkpath(joinpath(root, "outputs"))
open(joinpath(root, "outputs", "julia_context_summary.csv"), "w") do io
    println(io, "developmental_context,n," * join([m * "_mean" for m in metrics], ","))
    for c in contexts
        sub = rows[rows[:, col("developmental_context")] .== c, :]
        vals = [mean(parse.(Float64, sub[:, col(m)])) for m in metrics]
        @printf(io, "%s,%d,%s\n", c, size(sub, 1), join(round.(vals, digits=4), ","))
    end
end
println("Wrote Julia outputs.")
