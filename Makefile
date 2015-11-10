.PHONY: deps-test clean unit upload

clean:
	@echo "Cleaning up build and *.pyc files..."
	@find . -name "*.pyc" -delete
	@rm -rf .coverage
	@rm -rf ./build
	@rm -rf ./dist
	@rm -rf ./cover
	@rm -rf ./MANIFEST
	@echo "Done!"

test: clean
	@pip install setuptools\>=17
	@python ./setup.py test

upload:
	@python ./setup.py sdist upload -r pypi
