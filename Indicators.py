import backtrader as bt

class Indicators:

    # DONCHIAN CHANNEL
    @staticmethod
    def donchian_channels(data, entry_period, exit_period):
        donchian_entry = bt.indicators.DonchianChannel(data.close, period=entry_period)  # Open position
        donchian_exit = bt.indicators.DonchianChannel(data.close, period=exit_period)  # Close position
        return donchian_entry, donchian_exit

    # AVERAGE TRUE RANGE (ATR)
    @staticmethod
    def atr(data, atr_period):
        return bt.indicators.AverageTrueRange(data, period=atr_period)
