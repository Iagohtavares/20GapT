import os
from celery import Celery


app = Celery(include=('tasks',))
# app.conf.beat_schedule = {
#     'refresh': {
#         'task': 'refresh',
#         'schedule': float(os.environ['NEWSPAPER_SCHEDULE']),
#         'args': (os.environ['NEWSPAPER_URLS'].split(','),)
#     },
# }

app.conf.beat_schedule = {
    'get_values': {
        'task': 'get_values',
        'schedule': 300.0,
        'args': ()
    },
}
