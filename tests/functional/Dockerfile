FROM python:3.10

WORKDIR .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip install --upgrade pip \
      && pip install -r requirements.txt

COPY . ./tests/functional
