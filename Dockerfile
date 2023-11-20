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

RUN groupadd -r acait -g 1000 && \
    useradd -u 1000 -rm -g acait -d /home/acait -s /bin/bash -c "container user" acait && \
    chown -R acait:acait /app /home/acait

ADD --chown=acait:acait visits /app/visits/
ADD --chown=acait:acait db_config /app/db_config
ADD --chown=acait:acait setup.py requirements.txt /app/
ADD --chown=acait:acait scripts /scripts/
ADD --chown=acait:acait docker/app_init.sh docker/app_start.sh /scripts/

RUN chmod -R +x /scripts/ /app/visits/tasks/

USER acait

RUN . /app/bin/activate && pip install -r requirements.txt

CMD ["bash", "/scripts/app_start.sh"]

