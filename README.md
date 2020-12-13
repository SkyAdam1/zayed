# Zayed accelerator

## Требования

* [Python от v3.8](https://www.python.org/downloads/)
* [Pipenv](https://github.com/pypa/pipenv)
* [PostgreSQL](https://www.postgresql.org/download/)

## Установка зависимостей

```bash
pipenv install
```

## Создание базы данных

```sql
CREATE DATABASE <datebase name>
    WITH 
    OWNER = <user>
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1;
```

## Настройка проекта

./*settings.toml*

```toml
db_name = "<datebase name>"
db_host = "<datebase host>"
db_port = "<datebase port>"
```

./*.secrets.toml*

```toml
db_user = "<datebase owner name>"
db_password = "<datebase owner password>"
email_user = "<email>"
email_password = "<email password>"
```

## Миграции Django

```bash
python manage.py makemigrations
python manage.py migrate
```

## Создание пользователя

```bash
python manage.py createsuperuser
```
