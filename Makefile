.PHONY: init migrate upgrade

start: ## dockoer compose init
	docker-compose up
	docker-compose run app sh -c "flask db init && flask init_db"


migrate: ## Init and migrate database
	docker-compose run app flask db migrate


upgrade: ## Apply the upgrade to the database
	docker-compose run app flask db upgrade
