# Personality, Culture, and the Problem of Universality
# Julia workflow using standard-library tools plus DelimitedFiles/Statistics.

using DelimitedFiles
using Statistics
using Printf

root = normpath(joinpath(@__DIR__, ".."))
data_path = joinpath(root, "data", "synthetic_personality_culture_universality.csv")
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

culture_idx = col("culture_group")
traits = ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism", "honesty_humility"]
trait_indices = [col(t) for t in traits]

groups = unique(rows[:, culture_idx])

open(joinpath(outputs, "julia_group_summary.csv"), "w") do io
    println(io, "culture_group,n," * join([t * "_mean" for t in traits], ","))
    for g in groups
        mask = rows[:, culture_idx] .== g
        group_rows = rows[mask, :]
        means = Float64[]
        for idx in trait_indices
            vals = parse.(Float64, group_rows[:, idx])
            push!(means, mean(vals))
        end
        @printf(io, "%s,%d,%s\n", g, size(group_rows, 1), join(round.(means, digits=4), ","))
    end
end

println("Wrote Julia outputs to: ", outputs)
