.PHONY: validate python r sql clean

validate:
	bash validation/run_validation.sh

python:
	python3 python/analyze_person_situation_debate.py

r:
	Rscript r/analyze_person_situation_debate.R

sql:
	mkdir -p outputs
	sqlite3 outputs/person_situation_debate.sqlite < sql/schema_and_queries.sql

clean:
	rm -f outputs/*.csv outputs/*.txt outputs/*.sqlite outputs/*.json
