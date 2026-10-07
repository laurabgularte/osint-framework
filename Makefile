.PHONY: install test lint run

install:
	pip install -e .

test:
	pytest

run:
	osint-cli scan octocat