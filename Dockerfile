FROM python:3

RUN set -eux; \
  export DEBIAN_FRONTEND=noninteractive \
  && apt-get update \
  && apt-get install -y --no-install-recommends \
             jq \
             man \
             unzip \
             vim \
             zip \
             liblzo2-dev \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY requirements_post.txt /code/
RUN pip install -r requirements_post.txt
COPY . /code/

CMD ["python", "app.py"]
