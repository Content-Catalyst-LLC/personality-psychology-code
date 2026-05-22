using DelimitedFiles, Statistics, Printf
root = normpath(joinpath(@__DIR__, ".."))
raw = readdlm(joinpath(root, "data", "synthetic_psychodynamic_personality.csv"), ',', String)
header = vec(raw[1, :]); rows = raw[2:end, :]
col(name) = findfirst(==(name), header)
contexts = unique(rows[:, col("developmental_context")])
metrics = ["defensive_maturity", "attachment_insecurity", "self_relational_capacity", "character_integration", "symptom_distress"]
mkpath(joinpath(root, "outputs"))
open(joinpath(root, "outputs", "julia_developmental_context_summary.csv"), "w") do io
    println(io, "developmental_context,n," * join([m * "_mean" for m in metrics], ","))
    for c in contexts
        sub = rows[rows[:, col("developmental_context")] .== c, :]
        vals = [mean(parse.(Float64, sub[:, col(m)])) for m in metrics]
        @printf(io, "%s,%d,%s\n", c, size(sub, 1), join(round.(vals, digits=4), ","))
    end
end
println("Wrote Julia outputs.")
