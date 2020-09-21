init:
	pip install -r requirements-dev.txt
	pip install -e .
	pre-commit install

format:
	black . --line-length=100
	isort .
	flake8

check:
	pre-commit run --all-files

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info