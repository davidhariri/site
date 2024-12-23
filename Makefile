post:
	python cli.py

run:
	quart run --port=5001

test:
	pytest test_app.py

docker-build:
	docker build -t site .

docker-run:
	docker run --env-file .env -p 8000:8000 site