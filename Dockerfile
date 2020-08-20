FROM tiangolo/uwsgi-nginx-flask:python3.7
RUN apt-get update && apt-get upgrade -y
COPY ./app /app
RUN pip install -r /app/deps.txt
