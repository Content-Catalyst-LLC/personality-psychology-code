using DelimitedFiles, Statistics, Printf
root = normpath(joinpath(@__DIR__, ".."))
raw = readdlm(joinpath(root, "data", "synthetic_maladaptive_personality_structure.csv"), ',', String)
header = vec(raw[1, :]); rows = raw[2:end, :]
col(name) = findfirst(==(name), header)
contexts = unique(rows[:, col("clinical_context")])
metrics = ["functioning_impairment", "maladaptive_trait_burden", "clinical_severity", "clinical_liability"]
mkpath(joinpath(root, "outputs"))
open(joinpath(root, "outputs", "julia_clinical_context_summary.csv"), "w") do io
    println(io, "clinical_context,n," * join([m * "_mean" for m in metrics], ","))
    for c in contexts
        sub = rows[rows[:, col("clinical_context")] .== c, :]
        vals = [mean(parse.(Float64, sub[:, col(m)])) for m in metrics]
        @printf(io, "%s,%d,%s\n", c, size(sub, 1), join(round.(vals, digits=4), ","))
    end
end
println("Wrote Julia outputs.")
