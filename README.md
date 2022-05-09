# syllabit-backend


## Инструкция по запуску:

- Клонируем проект

- Создаем виртуальное окружение и активируем его:

```
python -m venv venv

win:
.\venv\Scripts\activate

linux:
source venv/bin/activate
```

- Устанавливаем зависимости:

```
pip install -r requirements.txt
```

- Применяем миграции:

```
python manage.py migrate
```

- Запускаем локальный сервер:

```
python manage.py runserver
```
