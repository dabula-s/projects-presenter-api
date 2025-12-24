build:
	docker compose build

up:
	docker copose up --build

load-seed:
	PYTHONPATH=src python -m cli database seed