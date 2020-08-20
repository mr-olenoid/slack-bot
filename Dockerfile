FROM tiangolo/uwsgi-nginx-flask:python3.7
RUN apt-get update && apt-get install -y ca-certificates
RUN update-ca-certificates
COPY ./app /app
RUN pip install -r /app/deps.txt
