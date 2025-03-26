<h1>Запуск проекта</h1>

<h4>
1. Создайте файл .env в корневой директории 
проекта и установите переменые согласно .env.example:
</h4>

```requirements
PROJECT_NAME=
SECRET_KEY=
DEBUG=

BOT_TOKEN=<Токен бота>
BOT_USERNAME=<Username бота>
MAX_MESSAGE_PER_SECOND=<Количество обрабатываемых сообщений в минуту(по умолчанию 1)

DB_NAME=<Название БД>
DB_USER=<Пользователь БД>
DB_PASSWORD=<Пароль от БД>
DB_HOST=db
DB_PORT=5432
```

<h4>
2. Запустите docker compose:
</h4>

```commandline
docker compose up --build -d
```


<h4>
3. Создайте суперпользователя админ панели:
</h4>

```commandline
docker exec -it {PROJECT_NAME из .env}_web python manage.py createsuperuser
```
<br>
<h4>
Готово! Админ панель доступна по адресу http://{IP сервера}/admin/
</h4>


