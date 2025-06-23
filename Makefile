build:
	docker compose build

up:
	docker compose up

down:
	docker compose down

clean:
	docker system prune -f

test: up
	python3 test/async_client_test.py
