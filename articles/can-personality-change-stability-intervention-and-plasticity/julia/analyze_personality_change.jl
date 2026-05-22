using DelimitedFiles, Statistics, Printf
root = normpath(joinpath(@__DIR__, ".."))
raw = readdlm(joinpath(root, "data", "synthetic_personality_change_intervention.csv"), ',', String)
header = vec(raw[1, :]); rows = raw[2:end, :]
col(name) = findfirst(==(name), header)
groups = unique(rows[:, col("intervention_group")])
waves = sort(unique(rows[:, col("wave_numeric")]))
traits = ["neuroticism", "extraversion", "conscientiousness", "openness", "agreeableness"]
mkpath(joinpath(root, "outputs"))
open(joinpath(root, "outputs", "julia_wave_summary.csv"), "w") do io
    println(io, "wave_numeric,intervention_group,n," * join([t * "_mean" for t in traits], ","))
    for w in waves
        for g in groups
            sub = rows[(rows[:, col("wave_numeric")] .== w) .& (rows[:, col("intervention_group")] .== g), :]
            if size(sub, 1) > 0
                vals = [mean(parse.(Float64, sub[:, col(t)])) for t in traits]
                @printf(io, "%s,%s,%d,%s\n", w, g, size(sub, 1), join(round.(vals, digits=4), ","))
            end
        end
    end
end
println("Wrote Julia outputs.")
