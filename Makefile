startapi:
	python engine/main.py

build:
	docker compose build -f docker-compose-local.yml

up:
	docker compose up -f docker-compose-local.yml

start: build up

