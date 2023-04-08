FROM python:3.11-slim-bullseye
MAINTAINER johnnylingo
WORKDIR /tmp
RUN pip3 install --upgrade pip
COPY ./requirements.txt ./
RUN pip3 install -r requirements.txt
ENV PORT=8080
ENV APP_DIR=/opt/www/code/python
ENV APP=app:app
RUN mkdir -p $APP_DIR
COPY *.py $APP_DIR
RUN mkdir -p /opt/db
COPY *.mmdb /opt/db
ENTRYPOINT cd $APP_DIR && uvicorn $APP --app-dir $APP_DIR --host 0.0.0.0 --port $PORT --reload
EXPOSE $PORT
