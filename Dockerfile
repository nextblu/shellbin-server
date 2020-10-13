FROM python:3.8.2
RUN useradd -ms /bin/bash admin
COPY --chown=admin:admin . /docker_app
WORKDIR /docker_app

RUN apt-get update -y && \
	apt-get upgrade -y && \
    apt-get -y install gcc mono-mcs -y && \
    apt-get install python3-dev default-libmysqlclient-dev -y && \
    apt-get install libev-dev -y && \
    rm -rf /var/lib/apt/lists/* && \
    pip install -r requirements.txt && \
    pip install mysqlclient

EXPOSE 3000

USER admin

CMD python ./app.py