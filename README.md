# Проектная работа 4 спринта

### Прогресс
:black_square_button: Dockerfile для билда бекенда для API. 
> :ballot_box_with_check: поднимается fastapi, redis и elasticsearch

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
