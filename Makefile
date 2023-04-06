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


.PYONY: db-migrate
db-migrate:
	alembic upgrade head
