## Before Commit

Run pre-commit:
```bash
make pre-commit
```

Run test:
```bash
make test
```

## Local Development

Run database and db migration
```bash
docker-compose up
```

Run usage examples interactively
```bash
docker exec -it chainmetareader_development_1 python -i usage.py
```
