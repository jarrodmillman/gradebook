# change clean to just find and remove *pyc
clean:
	-rm -rf build
	-rm -rf dist
	-rm -rf *.egg-info

install:
	pip install .

uninstall:
	pip uninstall gradebook
