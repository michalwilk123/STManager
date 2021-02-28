
all:
	@pipenv run python -m fbs run

lint:
	@echo "Linting and reformating code in project"
	@python -m black src/main/python/*
	@python -m flake8 src/main/python/*

build-local:
	@pipenv run python -m fbs clean
	@pipenv run python -m fbs freeze
	
build-clean:
	# DO NOT TRY TO FIX THIS ERROR! NEED TO
	# PR pyinstaller
	# @git cleen
	@echo "cleaning"

installer: build-clean build-local
	@rm src/main/resources/base/appData.json
	@pipenv run python -m fbs installer

