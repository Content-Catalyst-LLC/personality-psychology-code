# Julia analysis workflow for synthetic personality-creativity data.
# Uses CSV.jl and DataFrames.jl when available.

using Statistics

root = normpath(joinpath(@__DIR__, ".."))
data_path = joinpath(root, "data", "synthetic_personality_creativity.csv")
table_dir = joinpath(root, "outputs", "tables")
mkpath(table_dir)

try
    using CSV
    using DataFrames

    df = CSV.read(data_path, DataFrame)
    numeric_cols = [:openness, :intellect, :conscientiousness, :extraversion,
                    :agreeableness, :neuroticism, :persistence, :social_support,
                    :divergent_thinking, :creative_achievement, :everyday_creativity]

    summary_rows = DataFrame(variable=String[], mean=Float64[], sd=Float64[])
    for col in numeric_cols
        push!(summary_rows, (String(col), mean(df[!, col]), std(df[!, col])))
    end
    CSV.write(joinpath(table_dir, "julia_descriptive_summary.csv"), summary_rows)

    domain_summary = combine(groupby(df, :domain),
        :divergent_thinking => mean => :mean_divergent_thinking,
        :creative_achievement => mean => :mean_creative_achievement,
        :everyday_creativity => mean => :mean_everyday_creativity)
    CSV.write(joinpath(table_dir, "julia_domain_summary.csv"), domain_summary)

    println("Julia analysis complete. Outputs written to ", table_dir)
catch err
    open(joinpath(table_dir, "julia_notes.txt"), "w") do io
        println(io, "Julia package workflow skipped: ", err)
        println(io, "Install packages with: import Pkg; Pkg.add([\"CSV\", \"DataFrames\"])")
    end
    println("Julia workflow wrote package note to outputs/tables/julia_notes.txt")
end
