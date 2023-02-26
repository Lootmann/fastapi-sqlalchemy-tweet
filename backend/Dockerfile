FROM python:3.10-buster as builder
WORKDIR /code/
COPY ./requirements.txt /code/
RUN pip install -U pip && pip install -r requirements.txt

# Deploy
FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# from build to deploy container
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

# copy all ./app/* to /code/
COPY . /code/
