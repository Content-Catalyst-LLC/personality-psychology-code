.PHONY: validate python r sql clean

validate:
	bash validation/run_validation.sh

python:
	python3 python/analyze_temperament_personality.py

r:
	Rscript r/analyze_temperament_personality.R

sql:
	mkdir -p outputs
	sqlite3 outputs/temperament_personality.sqlite < sql/schema_and_queries.sql

clean:
	rm -f outputs/*.csv outputs/*.txt outputs/*.sqlite outputs/*.json
