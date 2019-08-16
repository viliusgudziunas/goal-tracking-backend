from . import celery


@celery.task
def add(x, y):
    print(" ")
    print(x + y)
    print(" ")
    return x + y
