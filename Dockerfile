FROM python:3.10.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install postgresql-client
RUN apt-get update && apt-get install -y postgresql-contrib


WORKDIR /usr/src/app/
COPY . /usr/src/app/

# update pip
RUN pip install --upgrade pip

# install dependencies
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

# allow execution on entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh