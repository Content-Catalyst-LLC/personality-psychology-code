.PHONY: validate python r sql

validate:
	bash validation/run_validation.sh

python:
	python3 python/analyze_personality_creativity.py

r:
	Rscript r/analyze_personality_creativity.R

sql:
	sqlite3 outputs/tables/personality_creativity.sqlite < sql/schema_and_queries.sql
