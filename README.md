# api_yatube

yatube - соц. сеть где авторы могут вести собственную страницу с постами. Другие пользователи могут оставлять комментарии под постами пользователя.
В данном проекте реализован API для yatube.

## Как запустить проект

Клонировать с git hub:
```
git clone git@github.com:maximov-569/api_final_yatube.git
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```
# Примеры запросов
## Пример 1
request: "/api/v1/posts/"

response:
```
{
        "count": 123,
	"next": "http://api.example.org/accounts/?offset=400&limit=100",
	"previous": "http://api.example.org/accounts/?offset=200&limit=100",
	"results": [
		{
			"id": 0,
			"author": "string",
			"text": "string",
			"pub_date": "2021-10-14T20:41:29.648Z",
			"image": "string",
			"group": 0
		}
		]
}
```
## Пример 2
request: api/v1/follow/
with body:
```
{
	"following": "SomeUser"
}
```

response:
```
{
	"following": "SomeUser",
	"user": "User"
}
```
