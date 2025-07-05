.PHONY: test

test: build-docker-test
	docker run tests

build-docker-test: Dockerfile
	docker build -t tests .
