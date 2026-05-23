.PHONY: validate python r sql clean

validate:
	bash validation/run_validation.sh

python:
	python3 python/analyze_lexical_structure.py

r:
	Rscript r/analyze_lexical_structure.R

sql:
	mkdir -p outputs
	sqlite3 outputs/lexical_structure.sqlite < sql/schema_and_queries.sql

clean:
	rm -f outputs/*.csv outputs/*.txt outputs/*.sqlite outputs/*.json
