MANAGE := FLASK_APP=run.py

.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

freeze: ## Pin current dependencies
	pipenv requirements > requirements.txt

build: ## build app
	docker-compose up -d --build --remove-orphans

up: ## docker up
	docker-compose up

down: ## docker down
	docker-compose down

down_v: ## docker down volume
	docker-compose down -v

docker-initdb: ## Init and create database
	docker-compose exec app $(MANAGE) flask db init && $(MANAGE) flask init_db

docker-migrate-db:  ## Generate an migration
	docker-compose exec app $(MANAGE) flask db migrate -m 'Intial Migration'

docker-upgrade-db: ## Apply the upgrade to the database
	docker-compose exec app $(MANAGE) flask db upgrade

docker-shell: ## Flask Shell Load
	docker-compose exec app $(MANAGE) flask shell

prune:
	docker system prune

enter_app:
	docker exec -it run bash
