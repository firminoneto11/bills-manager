cov := coverage run -m pytest
cov_port := 5500
url := http://localhost:$(cov_port)
app := conf.asgi:application

env:
	rm -rf venv/
	python3.12 -m venv venv

deps:
	poetry install --no-root

dev:
	uvicorn $(app) --reload --port 8000

cov:
	$(cov)
	coverage report

hcov:
	$(cov)
	coverage html
	python -c "import webbrowser; webbrowser.open_new_tab('$(url)')"
	python -m http.server -d .coverage/html-report $(cov_port)
