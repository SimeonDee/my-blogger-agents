install:
	pip install uv
	uv add -r requirements.txt

run-server:
	python main.py