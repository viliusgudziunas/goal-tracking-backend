from api import celery


@celery.task
def test():
    print("Hello")
