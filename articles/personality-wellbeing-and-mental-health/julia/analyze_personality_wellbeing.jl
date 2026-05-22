# Personality, Wellbeing, and Mental Health
# Julia workflow using standard-library tools plus DelimitedFiles/Statistics.

using DelimitedFiles
using Statistics
using Printf

root = normpath(joinpath(@__DIR__, ".."))
data_path = joinpath(root, "data", "synthetic_personality_wellbeing_mental_health.csv")
outputs = joinpath(root, "outputs")
mkpath(outputs)

raw = readdlm(data_path, ',', String)
header = vec(raw[1, :])
rows = raw[2:end, :]

function col(name)
    idx = findfirst(==(name), header)
    idx === nothing && error("Missing column: $name")
    return idx
end

context_idx = col("life_context")
metrics = ["wellbeing_score", "distress_score", "flourishing_score", "perceived_support", "stress_burden"]
metric_indices = [col(m) for m in metrics]

contexts = unique(rows[:, context_idx])

open(joinpath(outputs, "julia_life_context_summary.csv"), "w") do io
    println(io, "life_context,n," * join([m * "_mean" for m in metrics], ","))
    for c in contexts
        mask = rows[:, context_idx] .== c
        context_rows = rows[mask, :]
        means = Float64[]
        for idx in metric_indices
            vals = parse.(Float64, context_rows[:, idx])
            push!(means, mean(vals))
        end
        @printf(io, "%s,%d,%s\n", c, size(context_rows, 1), join(round.(means, digits=4), ","))
    end
end

println("Wrote Julia outputs to: ", outputs)
