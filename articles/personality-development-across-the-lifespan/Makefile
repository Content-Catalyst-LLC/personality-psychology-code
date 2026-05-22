.PHONY: validate python r sql clean

validate:
	bash validation/run_validation.sh

python:
	python3 python/analyze_personality_lifespan.py

r:
	Rscript r/analyze_personality_lifespan.R

sql:
	mkdir -p outputs
	sqlite3 outputs/personality_lifespan.sqlite < sql/schema_and_queries.sql

clean:
	rm -f outputs/*.csv outputs/*.txt outputs/*.sqlite outputs/*.json
