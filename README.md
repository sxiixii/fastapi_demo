# Проектная работа 4 спринта

репозитории:

- [ETL](https://github.com/sxiixii/s4_etl)
- [API](https://github.com/sxiixii/async_api)
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
### Запуск ETL + API
- запустит все контейнеры
    ```commandline 
    make base_setup_run 
    ```
    *После запуска должна открываться страница с документацией [openapi](http://localhost:80/api/openapi) или [redoc](http://localhost:80/api/redoc)*

- удалит все контейнеры
   ```commandline 
   make base_setup_stop 
   ```
___
### Тесты
#### Postman
- Тесты для Postman находятся в корне проекта. Файл `APItests.postman_collection.json`

#### Функциональные тесты
- Возможны сценарии запуска тестов:
  - Запуск и анализ тестов непосредственно в тестовом окружении (*по умолчанию запускаются все тесты из папки tests/funcrional/src*)
    ```commandline
    make test_docker_setup
    ```
    *команда запустит и выведет результат тестов*
  - Запуск тестового окружения с последующим самостоятельным запуском тестов с нужными параметрами     
    ```commandline
    make docker_setup_run
    make venv
    pytest /tests/functional/test_film_api.py::test_films_search --vv --setup-show --disable-warnings
    ```
- Удалить тестовое окружение можно командой:
  ```commandline
  make stop_docker_setup
  ```