clean:
	-rm -rf build
	-rm -rf dist
	-rm -rf *.egg-info

install:
	python setup.py install --user
