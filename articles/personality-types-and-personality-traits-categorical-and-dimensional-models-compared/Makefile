.PHONY: validate python r sql clean

validate:
	bash validation/run_validation.sh

python:
	python3 python/analyze_types_traits_dimensional_models.py

r:
	Rscript r/analyze_types_traits_dimensional_models.R

sql:
	mkdir -p outputs
	sqlite3 outputs/types_traits_dimensional_models.sqlite < sql/schema_and_queries.sql

clean:
	rm -f outputs/*.csv outputs/*.txt outputs/*.sqlite outputs/*.json
