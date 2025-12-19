# TODO Service (FastAPI + SQLite)

TODO-сервис на FastAPI с хранением задач в SQLite. 

## Функциональность

Эндпоинты:
- `POST /items` — создать задачу 
- `GET /items` — получить список всех задач
- `GET /items/{item_id}` — получить задачу по ID
- `PUT /items/{item_id}` — обновить задачу по ID
- `DELETE /items/{item_id}` — удалить задачу по ID

При запуске приложения таблица в SQLite создаётся автоматически, если её нет.

---

## Запуск локально


В корне проекта:

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
uvicorn app.main:app --reload 
```

## Запуск Docker

```bash
docker pull maximstep/todo-service

docker volume create todo_data

docker run -d \
  --name todo-service \
  -p 8000:80 \
  -v todo_data:/app/data \
  maximstep/todo-service
```

Затем доступ по ссылке:
- http://localhost:8000
- http://localhost:8000/docs (документация)