FROM python:3.10

WORKDIR .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip install --upgrade pip \
      && pip install -r requirements.txt

COPY . ./tests/functional

RUN chmod +x ./tests/functional/entrypoint.sh

ENTRYPOINT ["./tests/functional/entrypoint.sh"]
