yapf:
	yapf -vv -ir .
	isort -y

lint:
	flake8 .
	pydocstyle .
	mypy .

clean:
	find . | grep -E '(__pycache__|\.pyc|\.pyo$$)' | xargs rm -rf

test:
	pytest --cov=.

test-cov:
	pytest --cov=. --cov-report html --cov-report term

ci-test:
	pytest --cov=.

install:
	pip install -r requirements.txt
	python setup.py install

dev-install:
	pip install -r requirements-dev.txt
	python setup.py develop
