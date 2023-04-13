import json
import requests
from celery.utils.log import get_task_logger

import utils
import utils as connection

logger = get_task_logger(__name__)


def condition_1(low, high):
    const_20_mov_avg = json.loads(connection.to_redis().get('20_mov_avg'))

    if low <= const_20_mov_avg <= high:
        return True
    return False


def condition_2(t, low, high):
    first_candle_mean = connection.to_redis().get("first_candle_mean")

    top_model_function = utils.function(t) + utils.HIGHER_FACTOR * utils.STD
    inf_model_function = utils.function(t) - utils.HIGHER_FACTOR * utils.STD

    candle_mean = (low + high)/2
    if t == 0:
        connection.to_redis().set("first_candle_mean", json.dumps(candle_mean))
        return True

    std_avg = first_candle_mean - candle_mean
    if inf_model_function <= std_avg <= top_model_function:
        return True
    return False


def buy_condition(symbol_info):
    const_20_mov_avg = json.loads(connection.to_redis().get('20_mov_avg'))

    if symbol_info == const_20_mov_avg:
        print('COMPRAAAAAAAAAAAAAA')
        header = {
            'cache-control': 'no-cache',
            'Cache-Control': 'no-cache',
            'content-type': 'application/json',
            'Content-Type': 'application/json'
        }
        r = requests.get("http://192.168.0.0:8000/buy", verify=False, headers=header)
        if r.status_code in ['200', 200, '201', 201, '202', 202]:
            response = r.json()
            logger.info(response)
