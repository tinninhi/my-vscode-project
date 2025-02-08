from celery import Celery
from modules.enhanced_publisher import EnhancedPublisher

app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task(bind=True, max_retries=3)
def publish_task(self, platform, article):
    """自动发布任务"""
    try:
        publisher = EnhancedPublisher(platform)
        publisher.login_and_publish(article)
    except Exception as e:
        self.retry(exc=e, countdown=60*60)