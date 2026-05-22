.PHONY: validate python r sql clean

validate:
	bash validation/run_validation.sh

python:
	python3 python/analyze_narrative_identity.py

r:
	Rscript r/analyze_narrative_identity.R

sql:
	mkdir -p outputs
	sqlite3 outputs/narrative_identity.sqlite < sql/schema_and_queries.sql

clean:
	rm -f outputs/*.csv outputs/*.txt outputs/*.sqlite outputs/*.json
