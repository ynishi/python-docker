.PHONY: build bash usage
SRC=app.py
NAME=py_prj

usage:
	@echo usage:
	@echo 'build, bash, run SRC=$${source.py}'

build:
	docker build -t $(NAME) .

bash:
	docker run --rm -it -v $$(pwd):/code $(NAME) bash 

run:
	docker run --rm -it -v $$(pwd):/code $(NAME) python $(SRC)
