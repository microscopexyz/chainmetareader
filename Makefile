.PHONY: init
init:
	@python3 -m pip install -r requirements.txt

.PHONY: pre-commit
pre-commit:
	pre-commit run --all-files


.PHONY: test
test:
	pytest tests -v
