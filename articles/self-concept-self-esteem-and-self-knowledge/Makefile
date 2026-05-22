.PHONY: validate python r sql clean

validate:
	bash validation/run_validation.sh

python:
	python3 python/analyze_self_concept_self_esteem_self_knowledge.py

r:
	Rscript r/analyze_self_concept_self_esteem_self_knowledge.R

sql:
	mkdir -p outputs
	sqlite3 outputs/self_concept_self_esteem_self_knowledge.sqlite < sql/schema_and_queries.sql

clean:
	rm -f outputs/*.csv outputs/*.txt outputs/*.sqlite outputs/*.json
