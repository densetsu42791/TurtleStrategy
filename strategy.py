import backtrader as bt
import numpy as np
from datetime import datetime
from Indicators import Indicators


class Turtles(bt.Strategy):

        def log(self, txt, dt=None):
            dt = dt or self.data.datetime.datetime(0)
            dt_str = dt.strftime('%d.%m.%y')
            print(f'{dt_str} {txt}')

        def __init__(self):
            self.open = self.datas[0].open
            self.high = self.datas[0].high
            self.low = self.datas[0].low
            self.close = self.datas[0].close

        def next(self):
            self.log(f'High - {self.high[0]:.2f}')