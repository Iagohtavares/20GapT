import MetaTrader5 as mt5


def trunc(num, n):
    integer = int(num * (10**n))/(10**n)
    return float(integer)


def symbol_info_function(_type_):
    symbol_info = dict(mt5.symbol_info())
    return symbol_info[_type_]
