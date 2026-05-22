.PHONY: validate python r sql clean

validate:
	bash validation/run_validation.sh

python:
	python3 python/analyze_mbti_typology_vs_traits.py

r:
	Rscript r/analyze_mbti_typology_vs_traits.R

sql:
	mkdir -p outputs
	sqlite3 outputs/mbti_typology_vs_traits.sqlite < sql/schema_and_queries.sql

clean:
	rm -f outputs/*.csv outputs/*.txt outputs/*.sqlite outputs/*.json
