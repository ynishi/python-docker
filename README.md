# docker-python
python develop in docker
dockerhub: https://hub.docker.com/r/ynishi/python-tools/

# Usage
## build
```
make build
```
## bash
```
make bash
```
## run a python script
```
make run SRC=${source.py}
```
## docker-compose up
```
# after make build
docker-compose up
```
### exec one script
```
docker-compose exec py python sript.py
```
# LICENSE
* MIT, see LICENSE
