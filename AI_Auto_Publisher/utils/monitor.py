from prometheus_client import Counter

PUBLISH_SUCCESS = Counter('publish_success', '发布成功次数')
PUBLISH_FAILURE = Counter('publish_failure', '发布失败次数')

def track_publish(status):
    if status:
        PUBLISH_SUCCESS.inc()
    else:
        PUBLISH_FAILURE.inc()