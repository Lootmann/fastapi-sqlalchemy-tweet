FROM python:3.10-buster as builder

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /api/

COPY ./requirements.txt /api/

RUN pip install -U pip setuptools wheel \
  && pip install -r requirements.txt \
  && rm -rf /root/.cache/pip

# Deploy
FROM python:3.10-slim-buster
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY . /api/
