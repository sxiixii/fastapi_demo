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
*После запуска должна открываться страница с документацией [openapi](http://localhost:80/api/openapi) или [redoc](http://localhost:80/api/redoc)*
___
### Тесты
#### Postman
Тесты для Postman находятся в корне проекта. Файл `APItests.postman_collection.json`

#### Функциональные тесты
Возможны два сценария запуска тестов:
1. Запуск в Docker. Для этого перейти `tests/functional` и выполнить `docker compose up -d`. Для корректной работы тестов необходимо заполнить файл `.env.docker`, которые находится в `tests/functional`, переменными окружения согласно шаблону.
2. Запуск локально. Для этого нужно убедиться, что остальные сервисы запущены в Docker. Затем перейти в `tests/functional` и выполнить команду ` pytest --disable-warnings ./src`. Для локального запуска необходимо заполнить файл `.env`, который находится в `tests/functional`, переменными окружения согласно шаблону
