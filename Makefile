.PHONY: deps-test clean unit upload

deps-test:
	@pip install -r test_requirements.txt

clean:
	@echo "Cleaning up build and *.pyc files..."
	@find . -name "*.pyc" -delete
	@rm -rf .coverage
	@rm -rf ./build
	@rm -rf ./dist
	@rm -rf ./cover
	@rm -rf ./MANIFEST
	@echo "Done!"

test: clean deps-test
	@nosetests -vv -s tests

upload:
	@python ./setup.py sdist upload -r pypi
