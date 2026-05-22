using DelimitedFiles, Statistics, Printf
root = normpath(joinpath(@__DIR__, ".."))
raw = readdlm(joinpath(root, "data", "synthetic_selfhood_agency_identity.csv"), ',', String)
header = vec(raw[1, :]); rows = raw[2:end, :]
col(name) = findfirst(==(name), header)
contexts = unique(rows[:, col("identity_context")])
metrics = ["temporal_self_continuity", "situated_agency_index", "social_recognition", "external_constraint", "identity_integration", "well_being"]
mkpath(joinpath(root, "outputs"))
open(joinpath(root, "outputs", "julia_identity_context_summary.csv"), "w") do io
    println(io, "identity_context,n," * join([m * "_mean" for m in metrics], ","))
    for c in contexts
        sub = rows[rows[:, col("identity_context")] .== c, :]
        vals = [mean(parse.(Float64, sub[:, col(m)])) for m in metrics]
        @printf(io, "%s,%d,%s\n", c, size(sub, 1), join(round.(vals, digits=4), ","))
    end
end
println("Wrote Julia outputs.")
