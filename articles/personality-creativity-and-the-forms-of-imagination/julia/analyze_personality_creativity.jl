# Julia workflow for synthetic personality-creativity data.
# Run from article directory:
# julia julia/analyze_personality_creativity.jl

using CSV
using DataFrames
using Statistics
using GLM
using StatsModels

article_dir = normpath(joinpath(@__DIR__, ".."))
data_path = joinpath(article_dir, "data", "synthetic_personality_creativity.csv")
table_dir = joinpath(article_dir, "outputs", "tables")
mkpath(table_dir)

df = CSV.read(data_path, DataFrame)

numeric_vars = [
    :openness,
    :intellect,
    :conscientiousness,
    :extraversion,
    :agreeableness,
    :neuroticism,
    :persistence,
    :social_support,
    :divergent_thinking,
    :creative_achievement,
    :everyday_creativity,
]

summary_rows = DataFrame(
    variable = String[],
    mean = Float64[],
    sd = Float64[],
)

for var in numeric_vars
    push!(summary_rows, (String(var), mean(df[!, var]), std(df[!, var])))
end

CSV.write(joinpath(table_dir, "julia_descriptive_statistics.csv"), summary_rows)

model_dt = lm(@formula(divergent_thinking ~ openness + intellect + conscientiousness + extraversion + agreeableness + neuroticism), df)
model_ca = lm(@formula(creative_achievement ~ openness + intellect + conscientiousness + persistence + social_support), df)

println("Divergent-thinking model:")
println(coeftable(model_dt))

println("\nCreative-achievement model:")
println(coeftable(model_ca))
