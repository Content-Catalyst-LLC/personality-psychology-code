.PHONY: validate python r sql clean

validate:
	bash validation/run_validation.sh

python:
	python3 python/analyze_traits_character.py

r:
	Rscript r/analyze_traits_character.R

sql:
	mkdir -p outputs
	sqlite3 outputs/traits_character.sqlite < sql/schema_and_queries.sql

clean:
	rm -f outputs/*.csv outputs/*.txt outputs/*.sqlite outputs/*.json
