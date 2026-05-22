.PHONY: validate python r sql clean

validate:
	bash validation/run_validation.sh

python:
	python3 python/analyze_behavior_genetics_personality.py

r:
	Rscript r/analyze_behavior_genetics_personality.R

sql:
	mkdir -p outputs
	sqlite3 outputs/behavior_genetics_personality.sqlite < sql/schema_and_queries.sql

clean:
	rm -f outputs/*.csv outputs/*.txt outputs/*.sqlite outputs/*.json
