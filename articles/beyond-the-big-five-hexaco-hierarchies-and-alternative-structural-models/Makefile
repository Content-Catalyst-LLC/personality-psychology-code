.PHONY: validate python r sql clean

validate:
	bash validation/run_validation.sh

python:
	python3 python/analyze_alternative_structures.py

r:
	Rscript r/analyze_alternative_structures.R

sql:
	mkdir -p outputs
	sqlite3 outputs/alternative_structures.sqlite < sql/schema_and_queries.sql

clean:
	rm -f outputs/*.csv outputs/*.txt outputs/*.sqlite outputs/*.json
