run:
	@pipenv run python -m fbs run


lint:
	@echo "Linting and reformating code in project"
	@python -m black src/main/python/* --line-length=79
	@python -m flake8 src/main/python/*


installer: install_local
	@pipenv run python -m fbs installer


install_local: install_packages
	@pipenv run python -m fbs clean
	@pipenv run python -m fbs freeze
	

install_packages:
	@command -v pipenv &> /dev/null || pip install pipenv
	@pipenv install