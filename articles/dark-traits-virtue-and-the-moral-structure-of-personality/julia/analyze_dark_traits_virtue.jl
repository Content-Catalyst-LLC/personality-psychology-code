using DelimitedFiles, Statistics, Printf
root = normpath(joinpath(@__DIR__, ".."))
raw = readdlm(joinpath(root, "data", "synthetic_dark_traits_virtue_personality.csv"), ',', String)
header = vec(raw[1, :]); rows = raw[2:end, :]
col(name) = findfirst(==(name), header)
contexts = unique(rows[:, col("institutional_context")])
metrics = ["dark_trait_burden", "virtue_relevant_tendency", "institutional_accountability", "unethical_behavior", "harm_indicator"]
mkpath(joinpath(root, "outputs"))
open(joinpath(root, "outputs", "julia_institutional_context_summary.csv"), "w") do io
    println(io, "institutional_context,n," * join([m * "_mean" for m in metrics], ","))
    for c in contexts
        sub = rows[rows[:, col("institutional_context")] .== c, :]
        vals = [mean(parse.(Float64, sub[:, col(m)])) for m in metrics]
        @printf(io, "%s,%d,%s\n", c, size(sub, 1), join(round.(vals, digits=4), ","))
    end
end
println("Wrote Julia outputs.")
