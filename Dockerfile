FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR ./code
ADD . /code
RUN python -m pip install -r requirements.txt --no-cache-dir 
VOLUME ["/code"]

