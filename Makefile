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
base_setup_run: clone_etl run_etl run_api

base_setup_stop:
	docker network prune -f && \
	docker compose -f docker-compose.yml stop && \
	docker compose -f _tmp/ETL/docker-compose.yml stop  && \
	docker network rm s4_network && \
	docker compose -f docker-compose.yml down --volumes && \
	docker compose -f _tmp/ETL/docker-compose.yml down --volumes  && \
	remove rm -rf ./_tmp/

docker_setup_run:
	docker compose -f tests/functional/docker-compose.yml up -d --build --wait

test_docker_setup:
	docker compose -f tests/functional/docker-compose.yml up -d --build --wait && \
	docker logs --follow tests

stop_docker_setup:
	docker compose -f tests/functional/docker-compose.yml stop && \
	docker compose -f tests/functional/docker-compose.yml down --volumes

make_venv:
	virtualenv venv && \
	. venv/bin/activate &&\
	pip install -r requirements.txt