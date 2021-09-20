FROM python:2

ARG DEBIAN_FRONTEND=noninteractive
RUN \
  apt-get update && \
  apt-get install -y make \
  && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/

RUN pip install --no-cache \
    git+https://github.com/Simperium/simperium-python.git

COPY . /usr/src/simplenote-backup/
WORKDIR /usr/src/simplenote-backup/

CMD [ "make" ]
