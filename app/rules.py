import json

import utils
import utils as connection


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
