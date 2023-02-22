.PHONY: init
init:
	@python3 -m pip install -r requirements.txt

.PHONE: pre-commit
pre-commit:
	pre-commit
