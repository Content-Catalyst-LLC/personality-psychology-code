# Personality and Institutions: Leadership, Bureaucracy, and Social Order
# Julia workflow using standard-library tools plus DelimitedFiles/Statistics.

using DelimitedFiles
using Statistics
using Printf

root = normpath(joinpath(@__DIR__, ".."))
data_path = joinpath(root, "data", "synthetic_personality_institutions_bureaucracy.csv")
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

unit_idx = col("institutional_unit")
metrics = ["bureaucratic_fit", "discretion_level", "accountability_strength", "institutional_performance", "institutional_trust"]
metric_indices = [col(m) for m in metrics]

units = unique(rows[:, unit_idx])

open(joinpath(outputs, "julia_institutional_unit_summary.csv"), "w") do io
    println(io, "institutional_unit,n," * join([m * "_mean" for m in metrics], ","))
    for u in units
        mask = rows[:, unit_idx] .== u
        unit_rows = rows[mask, :]
        means = Float64[]
        for idx in metric_indices
            vals = parse.(Float64, unit_rows[:, idx])
            push!(means, mean(vals))
        end
        @printf(io, "%s,%d,%s\n", u, size(unit_rows, 1), join(round.(means, digits=4), ","))
    end
end

println("Wrote Julia outputs to: ", outputs)
