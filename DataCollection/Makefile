.PHONY: help guard-virtual-env basedependencies env clean

guard-virtual-env: ## Exits if python virtual environment is not set
	@ if [ "${VIRTUAL_ENV}" = "" ]; then \
		echo "Virtual environment is not active. Activate with 'source env/bin/activate'"; \
		exit 1; \
	fi

clean: ## Removes all build artifacts
	for build_dir_glob in \
		build \
		dist \
		.eggs \
		*.egg-info \
		*.pyc \
		*.pyo \
		*~ \
		__pycache__ \
		.pytest_cache \
		.coverage \
		htmlcov; \
	do find . -name "$$build_dir_glob" -exec rm -fr {} +; done

basedependencies: guard-virtual-env clean
	pip3 install --upgrade pip setuptools wheel

dependencies: basedependencies
	pip3 install -r requirements.txt

install: basedependencies
	pip3 install .

development: dependencies
	pip3 install -e .



