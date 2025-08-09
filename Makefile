.PHONY: all clean install test

# # Default target
# all: install test

# # Install dependencies
# install:
# 	pip install -r requirements.txt

# # Run tests
# test:
# 	python -m pytest tests/

# Clean build artifacts
deepclean:
	docker compose down --volumes --remove-orphans
	-docker rmi $$(docker images --filter "dangling=true" -q --no-trunc)

# Watch run the application
run-watch:
	docker compose -f docker-compose.yml up --watch

run:
	docker compose -f docker-compose.yml up

# Rebuild and run
rebuild-and-run:
	docker compose -f docker-compose.yml up --build -d

# # Development dependencies
# dev-install:
# 	pip install -r requirements-dev.txt

# # Format code
# format:
# 	black .
# 	isort .

# # Check code style
# lint:
# 	flake8 .
# 	black . --check
# 	isort . --check

# .DEFAULT_GOAL := all