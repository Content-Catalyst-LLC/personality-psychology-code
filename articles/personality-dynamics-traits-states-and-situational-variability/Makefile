.PHONY: validate python r sql clean

validate:
	bash validation/run_validation.sh

python:
	python3 python/analyze_personality_dynamics.py

r:
	Rscript r/analyze_personality_dynamics.R

sql:
	mkdir -p outputs
	sqlite3 outputs/personality_dynamics.sqlite < sql/schema_and_queries.sql

clean:
	rm -f outputs/*.csv outputs/*.txt outputs/*.sqlite outputs/*.json
