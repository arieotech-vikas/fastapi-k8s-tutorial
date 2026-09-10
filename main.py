import json
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import engine, SessionLocal, Base
from models import Task
from cache import redis_client

Base.metadata.create_all(bind=engine)

app = FastAPI()

CACHE_KEY = "tasks:all"
CACHE_TTL_SECONDS = 30

tasks = []

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/tasks")
def list_tasks(db: Session = Depends(get_db)):
    cached = redis_client.get(CACHE_KEY)
    if cached:
        return {"source": "cache", "tasks": json.loads(cached)}

    tasks = db.query(Task).all()
    tasks_data = [{"id": t.id, "title": t.title, "done": t.done} for t in tasks]
    redis_client.set(CACHE_KEY, json.dumps(tasks_data), ex=CACHE_TTL_SECONDS)
    return {"source": "db", "tasks": tasks_data}
    


@app.post("/tasks")
def create_task(title: str, db: Session = Depends(get_db)):
    task = Task(title=title)
    db.add(task)
    db.commit()
    db.refresh(task)
    redis_client.delete(CACHE_KEY)
    return task
