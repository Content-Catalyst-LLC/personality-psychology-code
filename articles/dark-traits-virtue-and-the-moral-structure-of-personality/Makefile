.PHONY: validate python r sql clean

validate:
	bash validation/run_validation.sh

python:
	python3 python/analyze_dark_traits_virtue.py

r:
	Rscript r/analyze_dark_traits_virtue.R

sql:
	mkdir -p outputs
	sqlite3 outputs/dark_traits_virtue.sqlite < sql/schema_and_queries.sql

clean:
	rm -f outputs/*.csv outputs/*.txt outputs/*.sqlite outputs/*.json
