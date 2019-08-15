from . import celery


@celery.task
def temp():
    print(" ")
    print("Hello")
    print(" ")
