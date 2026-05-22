using DelimitedFiles, Statistics, Printf
root = normpath(joinpath(@__DIR__, ".."))
raw = readdlm(joinpath(root, "data", "synthetic_personality_twin_data.csv"), ',', String)
header = vec(raw[1, :]); rows = raw[2:end, :]
col(name) = findfirst(==(name), header)
zygosities = unique(rows[:, col("zygosity")])
metrics = ["trait_mean", "trait_difference", "family_stress", "social_support", "socioeconomic_security", "nonshared_environment_index", "gxe_marker", "rge_marker"]
mkpath(joinpath(root, "outputs"))
open(joinpath(root, "outputs", "julia_zygosity_summary.csv"), "w") do io
    println(io, "zygosity,n_pairs," * join([m * "_mean" for m in metrics], ","))
    for z in zygosities
        sub = rows[rows[:, col("zygosity")] .== z, :]
        vals = [mean(parse.(Float64, sub[:, col(m)])) for m in metrics]
        @printf(io, "%s,%d,%s\n", z, size(sub, 1), join(round.(vals, digits=4), ","))
    end
end
println("Wrote Julia outputs.")
