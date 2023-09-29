FROM ubuntu:20.04 as legacy-compass-container
ENV PYTHONUNBUFFERED 1
ENV TZ America/Los_Angeles

RUN apt-get update -y && apt-get -y install curl lsb-release && \
    curl https://packages.microsoft.com/keys/microsoft.asc | tee /etc/apt/trusted.gpg.d/microsoft.asc && \
    curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list | tee /etc/apt/sources.list.d/mssql-release.list

# Install system dependencies
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y && \
  apt-get upgrade -y && \
  apt-get dist-upgrade -y && \
  apt-get clean && \
  apt-get install -y \
  build-essential \
  python-setuptools \
  python3.8-dev \
  python3-venv \
  python3-pip

RUN ACCEPT_EULA=Y apt-get install -y msodbcsql18 mssql-tools18 unixodbc-dev

RUN echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc

ADD scripts /scripts
RUN chmod -R +x /scripts

RUN python3 -m venv /app/

RUN . /app/bin/activate && \
    /app/bin/pip install wheel gunicorn django-prometheus croniter pyodbc

CMD ["bash", "-c", "tail -f /dev/null"]