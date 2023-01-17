# Проектная работа 4 спринта

репозитории:

- etl - ![ссылка](https://github.com/sxiixii/s4_etl)
- api - ![ссылка](https://github.com/sxiixii/async_api)
---
### Для разработки
находясь в корне проекта - включи пре-коммит
```commandline
$ pre-commit install
$ pre-commit autoupdate
```
проверить работоспособность 
```commandline
$ pre-commit run --all-files
```
---
### Запуск 
```commandline
$ docker compose up -d --build
```
*После запуска должна открываться [страница с документацией](http://0.0.0.0:8000/api/openapi)*
