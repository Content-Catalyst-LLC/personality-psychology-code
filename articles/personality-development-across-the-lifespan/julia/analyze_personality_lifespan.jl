using DelimitedFiles, Statistics, Printf
root = normpath(joinpath(@__DIR__, ".."))
raw = readdlm(joinpath(root, "data", "synthetic_personality_lifespan.csv"), ',', String)
header = vec(raw[1, :]); rows = raw[2:end, :]
col(name) = findfirst(==(name), header)
stages = unique(rows[:, col("life_stage")])
traits = ["neuroticism", "extraversion", "conscientiousness", "openness", "agreeableness"]
mkpath(joinpath(root, "outputs"))
open(joinpath(root, "outputs", "julia_life_stage_summary.csv"), "w") do io
    println(io, "life_stage,n,age_mean," * join([t * "_mean" for t in traits], ","))
    for s in stages
        sub = rows[rows[:, col("life_stage")] .== s, :]
        vals = [mean(parse.(Float64, sub[:, col(t)])) for t in traits]
        age_mean = mean(parse.(Float64, sub[:, col("age")]))
        @printf(io, "%s,%d,%.4f,%s\n", s, size(sub, 1), age_mean, join(round.(vals, digits=4), ","))
    end
end
println("Wrote Julia outputs.")
