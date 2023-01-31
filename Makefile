.PHONY: clone_etl
clone_etl:
	mkdir -p _tmp && \
	cd _tmp/ && \
	git clone git@github.com:sxiixii/ETL.git

.PHONY: run_etl
run_etl:
	cp _tmp/ETL/etl/.env.template _tmp/ETL/etl/.env && \
	docker compose -f _tmp/ETL/docker-compose.yml up -d --build

.PHONY: run_api
run_api:
	docker compose -f docker-compose.yml up -d --build --wait

.PHONY: base_run
base_run: clone_etl run_etl run_api