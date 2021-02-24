
all:
	@pipenv run python -m fbs run

lint:
	@echo "Linting and reformating code in project"
	@python -m black src/main/python/*
	@python -m flake8 src/main/python/*

build-local:
	@pipenv run python -m fbs clean
	@pipenv run python -m fbs freeze

installer-platform-windows:
installer-platform-linux:
installer-platform-macos: