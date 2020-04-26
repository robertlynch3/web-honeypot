FROM mysql:latest

LABEL MAINTAINER Robert Lynch "rob@rlyn.ch"

ENV MYSQL_ROOT_PASSWORD 'honeypotR00t'
ENV MYSQL_ROOT_HOST '%'

ADD mysql/db.sql /db.sql
ADD mysql/init.sh /init.sh
RUN ["/bin/bash", "/init.sh"]