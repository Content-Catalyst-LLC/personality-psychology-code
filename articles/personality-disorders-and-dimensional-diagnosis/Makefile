.PHONY: validate python r sql clean

validate:
	bash validation/run_validation.sh

python:
	python3 python/analyze_dimensional_personality_disorders.py

r:
	Rscript r/analyze_dimensional_personality_disorders.R

sql:
	mkdir -p outputs
	sqlite3 outputs/dimensional_personality_disorders.sqlite < sql/schema_and_queries.sql

clean:
	rm -f outputs/*.csv outputs/*.txt outputs/*.sqlite outputs/*.json
