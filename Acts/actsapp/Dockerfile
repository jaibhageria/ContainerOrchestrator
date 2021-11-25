FROM alpine:3.7

ENV APP_DIR /acts_app
ENV TEAM_ID CC_144_169_128_180

RUN mkdir ${APP_DIR}
COPY ./acts ${APP_DIR}
#RUN mkdir -p /data/db

RUN apk update
RUN apk add --no-cache py3-pip
RUN pip3 install --upgrade pip
RUN apk add --no-cache openrc
RUN pip3 install -r /acts_app/requirements.txt
#RUN apk add mongodb
RUN apk add vim

EXPOSE 80
#EXPOSE 27017

WORKDIR ${APP_DIR}
#CMD ["mongod","--bind_ip","0.0.0.0","--fork","--logpath","/var/log/mongod.log",";","python3","mongo_users.py",";","python3","user_api.py"]
CMD ["sh", "-c", "python3 mongo_acts.py ; python3 acts_api.py"]
