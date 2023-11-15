FROM ubuntu:20.04 as app-container

WORKDIR /app/
ENV PYTHONUNBUFFERED 1

USER root

# install system dependencies
RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get dist-upgrade -y && \
    apt-get clean all && \
    apt-get install -y \
    hostname \
    locales \
    openssl \
    curl \
    wget \
    python-setuptools \
    build-essential\
    python-setuptools \
    python3.8-dev \
    python3-venv \
    python3-pip \
    libpq-dev \
    unixodbc-dev \
    freetds-dev

RUN apt-get update && apt-get install -y tdsodbc

RUN locale-gen en_US.UTF-8
# locale.getdefaultlocale() searches in this order
ENV LANGUAGE en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV LC_CTYPE en_US.UTF-8
ENV LANG en_US.UTF-8

# create python virtualenv
RUN python3 -m venv /app/

RUN /app/bin/pip install wheel croniter

ADD . /app/

RUN groupadd -r acait -g 1000 && \
    useradd -u 1000 -rm -g acait -d /home/acait -s /bin/bash -c "container user" acait && \
    chown -R acait:acait /app /home/acait && \
    chmod -R +x /app/scripts /app/visits/tasks

USER acait

RUN . /app/bin/activate && pip install -r requirements.txt

CMD ["bash", "/app/docker/app_start.sh"]

