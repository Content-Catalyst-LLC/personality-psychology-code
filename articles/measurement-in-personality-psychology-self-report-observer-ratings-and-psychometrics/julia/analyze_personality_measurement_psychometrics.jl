using DelimitedFiles, Statistics, Printf
root = normpath(joinpath(@__DIR__, ".."))
raw = readdlm(joinpath(root, "data", "synthetic_personality_measurement_data.csv"), ',', String)
header = vec(raw[1, :]); rows = raw[2:end, :]
col(name) = findfirst(==(name), header)
contexts = unique(rows[:, col("assessment_context")])
metrics = ["attention_check", "careless_response_risk", "social_desirability_pressure", "absolute_self_other_discrepancy", "method_effect_index", "reliability_context_score", "professional_reflection_score"]
mkpath(joinpath(root, "outputs"))
open(joinpath(root, "outputs", "julia_context_summary.csv"), "w") do io
    println(io, "assessment_context,n," * join([m * "_mean" for m in metrics], ","))
    for c in contexts
        sub = rows[rows[:, col("assessment_context")] .== c, :]
        vals = [mean(parse.(Float64, sub[:, col(m)])) for m in metrics]
        @printf(io, "%s,%d,%s\n", c, size(sub, 1), join(round.(vals, digits=4), ","))
    end
end
println("Wrote Julia outputs.")
