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

./*.env*

```env
settings = "dev"
secret_key = "cl^sglcth^0ixg&!$nnq9@*0ah(h2bb11$)0dgmwh2#-3v80g1"

db_name = ""
db_host = ""
db_port = ""
db_user = ""
db_password = ""

email_user = ""
email_password = ""
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
