using DelimitedFiles, Statistics, Printf
root = normpath(joinpath(@__DIR__, ".."))
raw = readdlm(joinpath(root, "data", "synthetic_values_strivings_direction.csv"), ',', String)
header = vec(raw[1, :]); rows = raw[2:end, :]
col(name) = findfirst(==(name), header)
contexts = unique(rows[:, col("value_context")])
metrics = ["self_transcendence", "self_enhancement", "openness_to_change", "conservation", "motivational_quality", "striving_conflict", "life_direction_coherence", "life_satisfaction"]
mkpath(joinpath(root, "outputs"))
open(joinpath(root, "outputs", "julia_values_strivings_context_summary.csv"), "w") do io
    println(io, "value_context,n," * join([m * "_mean" for m in metrics], ","))
    for c in contexts
        sub = rows[rows[:, col("value_context")] .== c, :]
        vals = [mean(parse.(Float64, sub[:, col(m)])) for m in metrics]
        @printf(io, "%s,%d,%s\n", c, size(sub, 1), join(round.(vals, digits=4), ","))
    end
end
println("Wrote Julia outputs.")
