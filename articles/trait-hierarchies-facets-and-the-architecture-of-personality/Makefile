.PHONY: validate python r sql clean

validate:
	bash validation/run_validation.sh

python:
	python3 python/analyze_trait_hierarchies.py

r:
	Rscript r/analyze_trait_hierarchies.R

sql:
	mkdir -p outputs
	sqlite3 outputs/trait_hierarchies.sqlite < sql/schema_and_queries.sql

clean:
	rm -f outputs/*.csv outputs/*.txt outputs/*.sqlite outputs/*.json
