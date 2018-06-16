# docker-python
python develop in docker

dockerhub: https://hub.docker.com/r/ynishi/python-tools/

## Usage
### build
```
make build
# with options
make build RESISTORY=myreg IMAGE=myimage
```
### push
```
make prepush
make push
```
### run python
```
docker-compose up
docker-compose exec jupyterlab python
```
or
```
docker run --rm -v $(pwd):/code ynishi/python-tools python
```
### common in dev
#### login jupyterlab
```
docker-compose up -d
docker-compose logs | grep token
# replace domain to localhost or accessible hostname to container and browse
```
#### exec one script
```
docker-compose exec jupyterlab python ${SCRIPT}
```
```
docker run --rm -v $(pwd):/code ynishi/python-tools python ${SCRIPT}
```
#### interactive
```
docker run --rm -it -v $(pwd):/code ynishi/python-tools [bash|ptipyton...]
```
#### autopep8 -- formatter
```
docker run --rm -it -v $(pwd):/code ynishi/python-tools autopep8 --in-place --aggressive --aggressive ${SRC}
```
# LICENSE
* MIT, see LICENSE

