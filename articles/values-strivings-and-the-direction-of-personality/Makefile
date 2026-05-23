.PHONY: validate python r sql clean

validate:
	bash validation/run_validation.sh

python:
	python3 python/analyze_values_strivings_direction.py

r:
	Rscript r/analyze_values_strivings_direction.R

sql:
	mkdir -p outputs
	sqlite3 outputs/values_strivings_direction.sqlite < sql/schema_and_queries.sql

clean:
	rm -f outputs/*.csv outputs/*.txt outputs/*.sqlite outputs/*.json
