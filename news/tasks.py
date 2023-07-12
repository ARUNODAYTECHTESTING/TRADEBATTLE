from core.celery import app

@app.task
def some_tasks():
    print("Execute me every minute please !!!")