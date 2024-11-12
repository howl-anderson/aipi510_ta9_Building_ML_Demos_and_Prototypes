FROM tiangolo/uwsgi-nginx-flask:python3.10
COPY ./app /app
ENV UWSGI_CHEAPER 2
ENV UWSGI_PROCESSES 8
RUN pip install -r /app/requirements.txt