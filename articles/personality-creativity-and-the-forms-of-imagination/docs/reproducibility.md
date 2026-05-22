# Reproducibility

## Minimal dependencies

Python:

```bash
pip install pandas numpy statsmodels matplotlib
```

R:

```r
install.packages(c("readr", "dplyr", "ggplot2", "broom"))
```

SQLite:

```bash
sqlite3 --version
```

Julia:

```julia
import Pkg
Pkg.add(["CSV", "DataFrames", "Statistics", "GLM", "StatsModels"])
```

## Recommended order

```bash
python3 python/analyze_personality_creativity.py
Rscript r/analyze_personality_creativity.R
sqlite3 outputs/tables/personality_creativity.sqlite < sql/schema_and_queries.sql
bash validation/run_validation.sh
```

## Expected outputs

```text
outputs/tables/python_correlation_matrix.csv
outputs/tables/python_model_coefficients.csv
outputs/tables/r_model_coefficients.csv
outputs/figures/python_openness_divergent_thinking.png
outputs/figures/python_openness_creative_achievement.png
outputs/figures/r_openness_divergent_thinking.png
outputs/figures/r_openness_creative_achievement.png
```
