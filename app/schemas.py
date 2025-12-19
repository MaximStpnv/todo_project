from typing import Optional 
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime 

#создаем схемы для данных 

#схема для валидации вывода тасков 
class STask(BaseModel):
    id:int  
    title:str = Field(..., min_length=1, max_length=100, description="Название задачи")
    description:Optional[str] = Field(None,max_length=2000, description="Описание задачи")
    completed: bool 
    created_at: datetime
    
    #разрешаем читать данные из ORM объектов
    model_config = ConfigDict(from_attributes=True)

#схема для валидации создания тасков 
class SCreateTask(BaseModel):
    title:str = Field(..., min_length=1, max_length=100, description="Название задачи")
    description:Optional[str] = Field(None, max_length=2000, description="Описание задачи")
    completed:bool = False

#схема для валидации обновления данных
class SUpdateTask(BaseModel):
    title:Optional[str] = Field(None, min_length=1, max_length=100, description="Название задачи")
    description:Optional[str] = Field(None, max_length=2000, description="Описание задачи")
    completed: Optional[bool] = None 