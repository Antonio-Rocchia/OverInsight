venv_dir = .venv

.PHONY: test
test:
	python -m unittest -v

.PHONY: build
build-linux:
	pyinstaller --name OverInsight-linux --onefile --noconsole -p src/ --hidden-import "babel.numbers" src/main.py

.PHONY: clean
clean:
	rm -rf ./build ./dist
