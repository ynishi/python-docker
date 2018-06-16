.PHONY: info build push lint test prepush
VERSION := $(shell git describe --tags --exact-match 2>/dev/null || echo latest)
ifeq (${VERSION}, head)
	TAG = latest
else
	TAG = ${VERSION}
endif
REGISTRY ?=
IMAGE ?= ynishi/python-tools
TARGET := ${REGISTRY}${IMAGE}:${TAG}

info:
	@echo "TARGET: ${TARGET}"

build:
	docker build -t $(TARGET) .

push: build
	$(if $(filter $(TAG), latest), $(warning push latest tag, recommend versioned target.))
	docker push ${TARGET}

lint: build
	docker run --rm ${TARGET} flake8

test: build
	docker run --rm ${TARGET} pytest

prepush: lint test
