.PHONY: validate python r sql clean

validate:
	bash validation/run_validation.sh

python:
	python3 python/analyze_ffm_architecture.py

r:
	Rscript r/analyze_ffm_architecture.R

sql:
	mkdir -p outputs
	sqlite3 outputs/ffm_architecture.sqlite < sql/schema_and_queries.sql

clean:
	rm -f outputs/*.csv outputs/*.txt outputs/*.sqlite outputs/*.json
