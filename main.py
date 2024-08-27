import backtrader as bt
import numpy as np
import pandas as pd
from datetime import datetime
from strategy import Turtles


start = '2023-01-01'
end = '2023-03-01'
# step = 0.01
# cash = 1000


cerebro = bt.Cerebro()
cerebro.addstrategy(Turtles)
data = bt.feeds.GenericCSVData(dataname='SBER.csv', separator=';', dtformat=('%d/%m/%y'), fromdate=datetime.strptime(start, '%Y-%m-%d'), todate=datetime.strptime(end, '%Y-%m-%d'), datetime=0, open=2, high=3, low=4, close=5, volume=6,)
cerebro.adddata(data)
cerebro.broker.setcash(100000)  # Настройка начального капитала

# Добавление анализаторов
# cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="trade_analyzer")
# cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name="sharpe_ratio")

results = cerebro.run()  # Запуск Backtrader

# Получение результатов анализаторов
# trade_analyzer = results[0].analyzers.trade_analyzer.get_analysis()
# sharpe_ratio = results[0].analyzers.sharpe_ratio.get_analysis()

# Вывод статистики
# print('Конечный баланс: %.2f' % cerebro.broker.getvalue())
# print('Всего сделок:', trade_analyzer.total.closed)
# print('Профитных сделок:', trade_analyzer.won.total)
# print('Убыточных сделок:', trade_analyzer.lost.total)
# print('Процент прибыльных сделок: %.2f%%' % (trade_analyzer.won.total / trade_analyzer.total.closed * 100))
# print('Sharpe Ratio:', sharpe_ratio['sharperatio'])
