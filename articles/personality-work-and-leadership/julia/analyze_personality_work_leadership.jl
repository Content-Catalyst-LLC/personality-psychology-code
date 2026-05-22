# Personality, Work, and Leadership
# Julia workflow using standard-library tools plus DelimitedFiles/Statistics.

using DelimitedFiles
using Statistics
using Printf

root = normpath(joinpath(@__DIR__, ".."))
data_path = joinpath(root, "data", "synthetic_personality_work_leadership.csv")
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

role_idx = col("role_family")
metrics = ["job_performance", "leadership_emergence", "leadership_effectiveness", "teamwork_quality", "burnout_risk"]
metric_indices = [col(m) for m in metrics]

roles = unique(rows[:, role_idx])

open(joinpath(outputs, "julia_role_family_summary.csv"), "w") do io
    println(io, "role_family,n," * join([m * "_mean" for m in metrics], ","))
    for r in roles
        mask = rows[:, role_idx] .== r
        role_rows = rows[mask, :]
        means = Float64[]
        for idx in metric_indices
            vals = parse.(Float64, role_rows[:, idx])
            push!(means, mean(vals))
        end
        @printf(io, "%s,%d,%s\n", r, size(role_rows, 1), join(round.(means, digits=4), ","))
    end
end

println("Wrote Julia outputs to: ", outputs)
