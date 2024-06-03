cov := coverage run -m pytest
cov_port := 5500
url := http://localhost:$(cov_port)
app := conf.asgi:application

env:
	rm -rf venv/
	python3.12 -m venv venv

deps:
	pip install --upgrade pip setuptools
	poetry install --no-root
	pip uninstall rich -y

dev:
	uvicorn conf.asgi:app --reload --port 8000

cov:
	$(cov)
	coverage report

hcov:
	$(cov)
	coverage html
	python -c "import webbrowser; webbrowser.open_new_tab('$(url)')"
	python -m http.server -d .coverage/html-report $(cov_port)

test:
	docker compose -f ./scripts/docker-compose-test.yaml up --build
	docker rm bills-manager-tests
	docker rmi scripts-app
	docker network rm scripts_default

local:
	docker compose -f ./scripts/docker-compose-local.yaml up --build
	docker rm bills-manager-local
	docker rmi scripts-app
	docker network rm scripts_default

makemigrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate
