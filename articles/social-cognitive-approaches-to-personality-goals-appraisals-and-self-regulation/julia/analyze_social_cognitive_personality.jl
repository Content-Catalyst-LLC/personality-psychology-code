using DelimitedFiles, Statistics, Printf
root = normpath(joinpath(@__DIR__, ".."))
raw = readdlm(joinpath(root, "data", "synthetic_social_cognitive_personality.csv"), ',', String)
header = vec(raw[1, :]); rows = raw[2:end, :]
col(name) = findfirst(==(name), header)
situations = unique(rows[:, col("situation_type")])
metrics = ["goal_activation", "threat_appraisal", "challenge_appraisal", "self_efficacy", "self_regulation", "prosocial_behavior", "avoidance_behavior", "task_persistence"]
mkpath(joinpath(root, "outputs"))
open(joinpath(root, "outputs", "julia_situation_summary.csv"), "w") do io
    println(io, "situation_type,n," * join([m * "_mean" for m in metrics], ","))
    for s in situations
        sub = rows[rows[:, col("situation_type")] .== s, :]
        vals = [mean(parse.(Float64, sub[:, col(m)])) for m in metrics]
        @printf(io, "%s,%d,%s\n", s, size(sub, 1), join(round.(vals, digits=4), ","))
    end
end
println("Wrote Julia outputs.")
