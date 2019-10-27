import os
from datetime import timedelta
from app import celery, create_app
from app.alarm_check import check_alarms

app = create_app(os.getenv('FLASK_CONFIG'))
app.app_context().push()


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(timedelta(seconds=5), check_alarms.s())
