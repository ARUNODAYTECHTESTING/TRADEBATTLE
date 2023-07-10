from core.celery import app

@app.task
def some_tasks():
    pass