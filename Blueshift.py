from blueshift.library.technicals.indicators import ema
from blueshift.api import symbol, order_percent, order, cancel_order, order_target_percent
from blueshift.api import set_stoploss, set_takeprofit, schedule_once
from blueshift.api import schedule_function, date_rules, time_rules, square_off
import talib as ta
import numpy as np
import pandas as pd

def initialize(context):
    context.params = {
            'stoploss':0.1,
            'takeprofit':0.5,
            'indicator_lookback': 150,
            'indicator_freq': '1d'
            }
    context.vix = symbol('INDIAVIX')
    context.nifty = symbol('NIFTY-I')
    context.stocks = ['RELIANCE', 'INFY']
    context.securities = [symbol(s) for s in context.stocks]

    
    schedule_function(
            enter, date_rules.every_day(), 
            time_rules.market_open(5))
    schedule_function(
            close_out, date_rules.every_day(), 
            time_rules.market_close(30))
    
    context.traded = False

def before_trading_start(context, data):
    context.entered = set()
    context.traded = False 

def enter(context, data):

    if context.traded:
        return
    close_out(context, data)


    s1_close = data.history(context.securities[0], 'close', 101, '1d')
    s2_close = data.history(context.securities[1], 'close', 101, '1d')
    ratio = np.array(s1_close) / np.array(s2_close)
    z_score_prev = (ratio[-2] - np.mean(ratio[:-1]))/np.std(ratio[:-1])
    z_score = (ratio[-1] - np.mean(ratio[1:]))/np.std(ratio[1:])

    k = 0.8
    
    if z_score > k and z_score_prev < k:
        print('detected 1')
        # order(context.securities[0], -size)
        order(context.securities[0], -0.5 * context.portfolio.cash / s1_close[-1])
        # order(context.securities[1], size)
        order(context.securities[1], 0.5 * context.portfolio.cash / s2_close[-1])
    if z_score < -k and z_score_prev > -k:
        print('detected 2')
        # order(context.securities[0], size)
        order(context.securities[0], 0.5 * context.portfolio.cash / s1_close[-1])
        # order(context.securities[1], -size)
        order(context.securities[1], -0.5 * context.portfolio.cash / s2_close[-1])
    if 0.1 > z_score > -0.1:
        print('detected 0')
        square_off(context.securities)

    context.traded = True
    schedule_once(set_targets)
    

def close_out(context, data):
    # square_off(context.securities)
    for oid in context.open_orders:
        cancel_order(oid)
        
    for asset in context.portfolio.positions:
        order(asset, 0)

def set_targets(context, data):
    for asset in context.portfolio.positions:
        if asset in context.entered:
            continue
        set_stoploss(asset, 'PERCENT', context.params['stoploss'])
        set_takeprofit(asset, 'PERCENT', context.params['takeprofit'])
        context.entered.add(asset)