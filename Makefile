MANAGE := FLASK_APP=./core/run.py

.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: venv
venv: ## Make a new virtual environment
	pipenv shell

.PHONY: install
install: venv ## Install or update dependencies
	pipenv install

freeze: ## Pin current dependencies
	pipenv requirements > ./core/requirements.txt

initdb: ## Init and create database
	$(MANAGE) flask db init && $(MANAGE) flask init_db

migrate: ## Generate an migration
	$(MANAGE) flask db migrate -m 'Intial Migration'

upgrade: ## Apply the upgrade to the database
	$(MANAGE) flask db upgrade

shell: ## Flask Shell Load
	$(MANAGE) flask shell
