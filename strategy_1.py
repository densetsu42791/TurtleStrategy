import backtrader as bt
import numpy as np
from datetime import datetime


class TurtleStrategy(bt.Strategy):
    params = (
        ('donchian_window_entry', 20),  # Период для входа
        ('donchian_window_exit', 10),  # Период для выхода
        ('atr_period', 20),  # Период для ATR (волатильности)
        ('risk_per_trade', 0.02),  # Риск на сделку (2% от капитала)
        ('units_limit', 4),  # Максимум 4 юнита на рынок
    )

    def __init__(self):
        # Индикаторы для стратегии
        self.donchian_entry = bt.indicators.DonchianChannel(
            self.data.close, period=self.params.donchian_window_entry)
        self.donchian_exit = bt.indicators.DonchianChannel(
            self.data.close, period=self.params.donchian_window_exit)
        self.atr = bt.indicators.AverageTrueRange(self.data, period=self.params.atr_period)

        # Переменные для управления позициями
        self.units = 0
        self.unit_size = 0
        self.last_trade_was_profitable = False

    def next(self):
        # Обновляем размер юнита на основе волатильности ATR
        self.unit_size = self.broker.get_cash() * self.params.risk_per_trade / self.atr[0]

        # Определение торговых сигналов
        if not self.position:  # Если нет открытой позиции
            if self.data.close[0] > self.donchian_entry.lines.high[0]:
                # Покупка при прорыве максимума за 20 дней
                if self.units < self.params.units_limit:
                    self.buy(size=self.unit_size)
                    self.units += 1
            elif self.data.close[0] < self.donchian_entry.lines.low[0]:
                # Продажа при прорыве минимума за 20 дней
                if self.units > -self.params.units_limit:
                    self.sell(size=self.unit_size)
                    self.units -= 1
        else:
            # Условия выхода из позиции
            if self.position.size > 0 and self.data.close[0] < self.donchian_exit.lines.low[0]:
                # Закрыть длинную позицию при прорыве минимума за 10 дней
                self.close()
                self.units = 0
            elif self.position.size < 0 and self.data.close[0] > self.donchian_exit.lines.high[0]:
                # Закрыть короткую позицию при прорыве максимума за 10 дней
                self.close()
                self.units = 0

    def notify_trade(self, trade):
        if trade.isclosed:
            if trade.pnl > 0:
                self.last_trade_was_profitable = True
            else:
                self.last_trade_was_profitable = False


# Создание экземпляра Cerebro для запуска стратегии
cerebro = bt.Cerebro()
cerebro.addstrategy(TurtleStrategy)

# Добавление данных (например, Yahoo Finance или CSV файл)
data = bt.feeds.YahooFinanceData(dataname='AAPL',
                                 fromdate=datetime(2018, 1, 1),
                                 todate=datetime(2020, 1, 1))
cerebro.adddata(data)

# Настройка начального капитала
cerebro.broker.setcash(100000)

# Добавление анализаторов
cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="trade_analyzer")
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name="sharpe_ratio")

# Запуск Backtrader
results = cerebro.run()

# Получение результатов анализаторов
trade_analyzer = results[0].analyzers.trade_analyzer.get_analysis()
sharpe_ratio = results[0].analyzers.sharpe_ratio.get_analysis()

# Вывод статистики
print('Конечный баланс: %.2f' % cerebro.broker.getvalue())
print('Всего сделок:', trade_analyzer.total.closed)
print('Профитных сделок:', trade_analyzer.won.total)
print('Убыточных сделок:', trade_analyzer.lost.total)
print('Процент прибыльных сделок: %.2f%%' % (trade_analyzer.won.total / trade_analyzer.total.closed * 100))
print('Sharpe Ratio:', sharpe_ratio['sharperatio'])
