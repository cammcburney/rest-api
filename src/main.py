from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel

app = FastAPI()

to_do_list = []

class Task(BaseModel):
    task_id: int
    task_name: str
    task_description: str | None = None


@app.get("/")
async def root():
    return {"Tasks": to_do_list}

@app.post("/tasks")
async def add_to_do_item(task: Task):
    to_do_list.append(task)
    return task

@app.get("/tasks/{task_id}")
async def get_task(task_id: int):
    if task_id > len(to_do_list):
        raise HTTPException(status_code=404, detail= f"Task {task_id} not found.")
    else:
        task = to_do_list[task_id]
        return task

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    for task in to_do_list:
        if task.task_id == task_id:
            to_do_list.pop(task_id)
            return {"task": f"task {task_id} removed"}
        
@app.put("/tasks/{task_id}")
async def update_task(task_id: int, updated_task: Task):
    for task in to_do_list:
        if task.task_id == task_id:
            task = updated_task
            to_do_list[task.task_id] = task
            return {"task": f"task {task_id} updated"}




if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)