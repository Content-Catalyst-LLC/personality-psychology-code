using DelimitedFiles, Statistics, Printf
root = normpath(joinpath(@__DIR__, ".."))
raw = readdlm(joinpath(root, "data", "synthetic_traits_character_morality.csv"), ',', String)
header = vec(raw[1, :]); rows = raw[2:end, :]
col(name) = findfirst(==(name), header)
contexts = unique(rows[:, col("evaluation_context")])
metrics = ["descriptive_trait_reliability", "moral_character_index", "moral_identity", "practical_judgment", "institutional_accountability"]
mkpath(joinpath(root, "outputs"))
open(joinpath(root, "outputs", "julia_evaluation_context_summary.csv"), "w") do io
    println(io, "evaluation_context,n," * join([m * "_mean" for m in metrics], ","))
    for c in contexts
        sub = rows[rows[:, col("evaluation_context")] .== c, :]
        vals = [mean(parse.(Float64, sub[:, col(m)])) for m in metrics]
        @printf(io, "%s,%d,%s\n", c, size(sub, 1), join(round.(vals, digits=4), ","))
    end
end
println("Wrote Julia outputs.")
