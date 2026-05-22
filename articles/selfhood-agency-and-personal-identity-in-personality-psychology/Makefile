.PHONY: validate python r sql clean

validate:
	bash validation/run_validation.sh

python:
	python3 python/analyze_selfhood_agency_identity.py

r:
	Rscript r/analyze_selfhood_agency_identity.R

sql:
	mkdir -p outputs
	sqlite3 outputs/selfhood_agency_identity.sqlite < sql/schema_and_queries.sql

clean:
	rm -f outputs/*.csv outputs/*.txt outputs/*.sqlite outputs/*.json
