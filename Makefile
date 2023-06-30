setup:
	python -m venv ./.venv
	.venv/bin/pip install -U numpy
run:
	.venv/bin/python ./main.py