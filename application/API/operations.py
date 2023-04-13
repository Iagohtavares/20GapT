import MetaTrader5 as mt5

from utils import connections


def makes_purchase():
    connect = connections.to_mt()
    if not connect:
        return mt5.last_error()

    lot = 0.1
    deviation = 5
    symbol = "EURUSD"
    symbol_info = mt5.symbol_info(symbol)

    point = symbol_info.point
    price = mt5.symbol_info_tick(symbol).ask

    data = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "sl": price - 100 * point,
        "tp": price + 100 * point,
        "deviation": deviation,
        "magic": 234000,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }
    result = mt5.order_send(data)

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("Order_send failed, retcode={}".format(result.retcode))
        return 'Deu ruim'
    return 'Deu bom'
