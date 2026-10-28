from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
     title="Task Manager API",
     description="Минимальный API для создания и получения задач."
)

class TaskCreate(BaseModel):
   """Модель данных для создания задачи."""

title: str = Field(
    min_length=3,
    max_length=100,
    description="Название задачи от 3 до 100 символов."
)
description: str | None = Field(
    default=None,
    description="Необязательное описание задачи."
)
priority: int = Field(
    ge=1,
    le=5,
    description="Приоритет задачи от 1 до 5."
)

class Task(TaskCreate):
  """Модель созданной задачи с уникальным идентификатором."""

  id: int = Field(
  description="Уникальный идентификатор задачи."
)
  
tasks: dict[int, Task] = {}
next_task_id = 1

@app.post( "/tasks",
           response_model=Task,
           status_code=201,
           summary="Создать задачу",
           description=( "Создаёт новую задачу. " "В ответе возвращаются данные задачи и её уникальный идентификатор." 
          ),
           responses={ 422: { "description": ( "Ошибка валидации: переданы некорректные данные " "или значения параметров находятся вне допустимого диапазона." 
                               ) 
                         } 
          } 
) 
def create_task(task: TaskCreate):
     global next_task_id

     new_task = Task(
        id=next_task_id,
        **task.model_dump()
     )

     tasks[next_task_id] = new_task
     next_task_id += 1

     return new_task

@app.get( 
     "/tasks/{task_id}",
      response_model=Task,
      summary="Получить задачу",
     description=( 
        "Возвращает задачу по её уникальному идентификатору. "
        "Если задача с указанным идентификатором не существует, " 
        "возвращается ошибка 404." 
     ), 
     responses={ 
          404: { "description": "Задача с указанным идентификатором не найдена.",
               "content": {
                   "application/json": { 
                      "example": {
                          "detail": "Задача не найдена." 
                     } 
               } 
          } 
   }, 
          422: { 
             "description": ( 
               "Ошибка валидации: идентификатор задачи " "имеет некорректный формат." 
               ) 
          } 
     }
 ) 
def get_task(task_id: int):
    if task_id not in tasks:
       raise HTTPException(
           status_code=404,
           detail="Задача не найдена."
           )
    return tasks[task_id]