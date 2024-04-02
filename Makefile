startapi:
	python engine/main.py

build:
	docker compose build

up:
	docker compose up

start: build up

