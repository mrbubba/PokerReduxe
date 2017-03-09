FROM python:2.7
ADD requirements.txt /app/requirements.txt
WORKDIR /app
RUN easy_install MySQL-python
RUN apt-get update && apt-get install -y python-mysqldb netcat
RUN pip install -r requirements.txt
# create unprivileged user
RUN adduser --disabled-password --gecos '' myuser