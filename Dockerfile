FROM 	python:latest
RUN 	apt-get update 
RUN 	apt-get install -y apache2 libapache2-mod-wsgi-py3 python3-pip

RUN 	pip3 install pymysql

WORKDIR /opt
RUN mkdir memecon
COPY . memecon/

VOLUME /opt/memecon
VOLUME /etc/apache2/sites-available

EXPOSE 80
EXPOSE 3306

ENTRYPOINT bash

