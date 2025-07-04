.PHONY: test

test:
	docker build -t tests .
	docker run --rm tests
