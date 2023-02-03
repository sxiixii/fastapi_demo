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