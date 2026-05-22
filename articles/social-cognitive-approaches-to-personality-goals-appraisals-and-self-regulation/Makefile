.PHONY: validate python r sql clean

validate:
	bash validation/run_validation.sh

python:
	python3 python/analyze_social_cognitive_personality.py

r:
	Rscript r/analyze_social_cognitive_personality.R

sql:
	mkdir -p outputs
	sqlite3 outputs/social_cognitive_personality.sqlite < sql/schema_and_queries.sql

clean:
	rm -f outputs/*.csv outputs/*.txt outputs/*.sqlite outputs/*.json
