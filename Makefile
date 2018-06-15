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

ptpy:
	docker run --rm -it -v $$(pwd):/code $(NAME) ptpython

ptipy:
	docker run --rm -it -v $$(pwd):/code $(NAME) ptipython

autopep:
	docker run --rm -it -v $$(pwd):/code $(NAME) autopep8 --in-place --aggressive --aggressive $(SRC)

jupyterlab:
	docker run --rm -it -v $$(pwd):/code -p 8888:8888 $(NAME) jupyter lab --ip=0.0.0.0 --allow-root
