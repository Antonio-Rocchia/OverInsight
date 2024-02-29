venv_dir = .venv

.PHONY: test
test:
	python -m unittest -v
