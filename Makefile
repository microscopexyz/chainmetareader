.PHONY: init
init:
	@python3 -m pip install -r requirements.txt

.PHONY: pre-commit
pre-commit:
	pre-commit run --all-files


.PHONY: test
test:
	pytest tests -v

.PHONY: db
db:
	docker volume create sql_data && docker run -d -e MYSQL_ROOT_PASSWORD=test -v sql_data_volume:/var/lib/mysql -p 3306:3306 mysql:8.0


.PHONY: db-migrate
db-migrate:
	alembic upgrade head

.PHONY: new-contributor
new-contributor:
	pip install -r ./scripts/new-contributor/requirements.txt && ./scripts/new-contributor/cli.py $(name)

.PHONY: doc-gen
doc-gen:
	pip install -r ./scripts/doc-gen/requirements.txt && ./scripts/doc-gen/cli.py $(name)
