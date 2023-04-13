import os
import json
import hashlib
import requests

from io import BytesIO
from celery.utils.log import get_task_logger
from minio import Minio
from minio.error import BucketAlreadyExists, BucketAlreadyOwnedByYou, NoSuchKey

import rules
import utils
from worker import app
import utils as connection


logger = get_task_logger(__name__)


@app.task(bind=True, name='get_values')
def get_values(self):
    header = {
        'cache-control': 'no-cache',
        'Cache-Control': 'no-cache',
        'content-type': 'application/json',
        'Content-Type': 'application/json'
    }
    r = requests.get("http://192.168.0.0:8000/data", verify=False, headers=header)
    if r.status_code in ['200', 200, '201', 201, '202', 202]:
        response = r.json()
        logger.info(response)

    const_20_mov_avg = json.loads(connection.to_redis().get('20_mov_avg'))
    logger.info('const_20_mov_avg')
    logger.info(const_20_mov_avg)
    logger.info('last_low')
    logger.info(response['low'])


@app.task(bind=True, name='save_article', queue='minio')
def save_article(self, bucket, key, text):

    minio_client = Minio(os.environ['MINIO_HOST'], 
        access_key=os.environ['MINIO_ACCESS_KEY'],
        secret_key=os.environ['MINIO_SECRET_KEY'],
        secure=False)

    try:
        minio_client.make_bucket(bucket, location="us-east-1")
    except BucketAlreadyExists:
        pass
    except BucketAlreadyOwnedByYou:
        pass

    hexdigest = hashlib.md5(text.encode()).hexdigest()
    try:
        st = minio_client.stat_object(bucket, key)
        update = st.etag != hexdigest
    except NoSuchKey as err:
        update = True

    if update:
        logger.info(f'Write {bucket}/{key} to minio')
        stream = BytesIO(text.encode())
        minio_client.put_object(bucket, key, stream, stream.getbuffer().nbytes)
