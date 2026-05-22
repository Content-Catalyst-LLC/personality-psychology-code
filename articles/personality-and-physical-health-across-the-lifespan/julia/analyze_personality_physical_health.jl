# Personality and Physical Health Across the Lifespan
# Julia workflow using standard-library tools plus DelimitedFiles/Statistics.

using DelimitedFiles
using Statistics
using Printf

root = normpath(joinpath(@__DIR__, ".."))
data_path = joinpath(root, "data", "synthetic_personality_physical_health_lifespan.csv")
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

age_band_idx = col("age_band")
metrics = ["physical_health_score", "functional_ability", "chronic_condition_burden", "stress_burden"]
metric_indices = [col(m) for m in metrics]

age_bands = unique(rows[:, age_band_idx])

open(joinpath(outputs, "julia_age_band_summary.csv"), "w") do io
    println(io, "age_band,n," * join([m * "_mean" for m in metrics], ","))
    for band in age_bands
        mask = rows[:, age_band_idx] .== band
        band_rows = rows[mask, :]
        means = Float64[]
        for idx in metric_indices
            vals = parse.(Float64, band_rows[:, idx])
            push!(means, mean(vals))
        end
        @printf(io, "%s,%d,%s\n", band, size(band_rows, 1), join(round.(means, digits=4), ","))
    end
end

println("Wrote Julia outputs to: ", outputs)
