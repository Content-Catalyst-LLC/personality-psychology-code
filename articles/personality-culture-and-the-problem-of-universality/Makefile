.PHONY: validate python r sql clean

validate:
	bash validation/run_validation.sh

python:
	python3 python/analyze_personality_culture_universality.py

r:
	Rscript r/analyze_personality_culture_universality.R

sql:
	mkdir -p outputs
	sqlite3 outputs/personality_culture_universality.sqlite < sql/schema_and_queries.sql

clean:
	rm -f outputs/*.csv outputs/*.txt outputs/*.sqlite outputs/*.json
