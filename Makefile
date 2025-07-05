.PHONY: test build-docker-test

test: build-docker-test
	docker run tests

build-docker-test: Dockerfile
	docker build -t tests .

docker-inspect:
	docker run -it tests /bin/bash