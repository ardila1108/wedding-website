build:
	docker build -t cb-wedding .

run:
	docker run --rm -p 8501:8501 --env-file .env cb-wedding

stop:
	docker stop $$(docker ps -q --filter ancestor=cb-wedding)

full_run:
	make build
	make run