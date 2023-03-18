all:
	cd docs/man && make
	python3 -m build

release:
	twine upload -r pypi dist/*

clean:
	rm -rf daily_cli.egg-info dist
