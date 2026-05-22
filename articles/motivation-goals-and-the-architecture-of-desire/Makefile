.PHONY: validate python r sql clean

validate:
	bash validation/run_validation.sh

python:
	python3 python/analyze_motivation_goals_desire.py

r:
	Rscript r/analyze_motivation_goals_desire.R

sql:
	mkdir -p outputs
	sqlite3 outputs/motivation_goals_desire.sqlite < sql/schema_and_queries.sql

clean:
	rm -f outputs/*.csv outputs/*.txt outputs/*.sqlite outputs/*.json
