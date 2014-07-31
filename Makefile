clean-pyc:
	find . -regex ".*\.pyc" -exec rm -rf "{}" \;

clean: clean-pyc

uninstall:
	pip uninstall gradebook

install: uninstall clean
	pip install .
