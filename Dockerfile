FROM python:3.7.2
RUN useradd -ms /bin/bash admin
COPY --chown=admin:admin . /docker_app
WORKDIR /docker_app

RUN apt-get update -y && \
    apt-get -y install gcc mono-mcs -y && \
    apt-get install python3-dev default-libmysqlclient-dev -y && \
    apt-get install libev-dev -y && \
    rm -rf /var/lib/apt/lists/*
# Multiple run -> docker will cache if no changes detected
RUN pip install -r requirements.txt && \
    pip install mysqlclient

EXPOSE 3000

USER admin

CMD python ./app.py
