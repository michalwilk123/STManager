all:
	@pipenv run python -m fbs run

install:
	@pipenv install

lint:
	@echo "Linting and reformating code in project"
	@python -m black src/main/python/* --line-length=79
	@python -m flake8 src/main/python/*

build: install
	@pipenv run python -m fbs clean
	@pipenv run python -m fbs freeze
	

installer: build
	@pipenv run python -m fbs installer

