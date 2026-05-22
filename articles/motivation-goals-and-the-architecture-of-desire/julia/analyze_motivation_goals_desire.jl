using DelimitedFiles, Statistics, Printf
root = normpath(joinpath(@__DIR__, ".."))
raw = readdlm(joinpath(root, "data", "synthetic_motivation_goals_desire.csv"), ',', String)
header = vec(raw[1, :]); rows = raw[2:end, :]
col(name) = findfirst(==(name), header)
contexts = unique(rows[:, col("motivation_context")])
metrics = ["approach_orientation", "status_orientation", "need_support", "motivational_quality", "goal_conflict", "persistence_score", "adaptive_disengagement", "well_being"]
mkpath(joinpath(root, "outputs"))
open(joinpath(root, "outputs", "julia_motivation_context_summary.csv"), "w") do io
    println(io, "motivation_context,n," * join([m * "_mean" for m in metrics], ","))
    for c in contexts
        sub = rows[rows[:, col("motivation_context")] .== c, :]
        vals = [mean(parse.(Float64, sub[:, col(m)])) for m in metrics]
        @printf(io, "%s,%d,%s\n", c, size(sub, 1), join(round.(vals, digits=4), ","))
    end
end
println("Wrote Julia outputs.")
