from .db import get_session, init_db, Task
from .schemas import STask, SCreateTask, SUpdateTask
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager 
from typing import List

@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Запуск TODO сервиса')
    init_db()
    yield
    print('Завершение работы сервиса')


app = FastAPI(title="TODO MAXIM STEPANOV", lifespan = lifespan, description="Сервис для отслеживания задач")

@app.get("/")
def hello():
    return {"message":"Привет друг!"}

#замечание!
#В return я делаю model_validate поскольку валидация через FastAPI происходит после закрытия сесии 
#Из-за этого появляется ошибка и объект ORM уже не доступен 
#Но я все равно пишу response_model = STask (по сути валидирую дважды)
#Затраты небольшие, но делаю я это в учебных целях 


@app.post("/items", response_model = STask, description="Добавление новых задач", status_code=201)
def add_task(payload:SCreateTask):
    with get_session() as session: 
        task = Task(title = payload.title, 
                    description = payload.description, 
                    completed = payload.completed) 
        
        session.add(task)
        
        #запись в бд но еще не зафиксирована пока не выщли из контекстного менеджера
        session.flush()
        
        last_task = session.query(Task).order_by(Task.id.desc()).first()
        # тут валидируем данные до закрытия сессии, чтобы не было ошибки
        return STask.model_validate(last_task)

@app.get("/items", response_model = List[STask], description="Получение всех задач")
def get_all_tasks():
    with get_session() as session: 
        all_tasks = session.query(Task).all()
        return [STask.model_validate(task) for task in all_tasks]


@app.get("/items/{item_id}", response_model = STask, description="Получение задачи по ID")
def get_task_by_id(item_id:int):
    with get_session() as session:
        task = session.query(Task).filter(Task.id == item_id).first()
        
        if not task:
            raise HTTPException(404, "Item not found")
        
        return STask.model_validate(task)

@app.put("/items/{item_id}", response_model = STask, description="Обновление полей по ID задачи")
def update_task_by_id(item_id:int, payload:SUpdateTask):
    with get_session() as session: 
        task_to_update = session.query(Task).filter(Task.id == item_id).first() 
        if not task_to_update:
            raise HTTPException(404, "Item not found")
        
        if payload.title:
            task_to_update.title = payload.title
        
        if payload.description:
            task_to_update.description = payload.description
        
        # вдруг мы захотим поменять на false пэтому делаем проверку is not None
        if payload.completed is not None:
            task_to_update.completed = payload.completed
        
        return STask.model_validate(task_to_update)

@app.delete("/items/{item_id}", description="Удаление задач ID", status_code=204)
def delete_task_by_id(item_id:int):
    with get_session() as session: 
        task_delete = session.query(Task).filter(Task.id == item_id).delete()
        if task_delete == 0:
            raise HTTPException(404, "Item not found")
        
        return None
    
