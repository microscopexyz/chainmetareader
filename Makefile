.PHONY: init
init:
	@python3 -m pip install -r requirements.txt

.PHONE: pre-commit
pre-commit:
	pre-commit run --all-files


.PHONE: test
test:
	pytest tests
