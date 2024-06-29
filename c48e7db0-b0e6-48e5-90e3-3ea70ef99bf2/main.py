from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    
    def __init__(self):
        # Example tickers for Korean companies - replace with actual tickers you want to trade
        self.tickers = ["005930", "000660", "035420"]  # Example: Samsung Electronics, SK Hynix, Naver
        self.data_list = []
        
    @property
    def interval(self):
        # Use daily trading data
        return "1day"
        
    @property
    def assets(self):
        return self.tickers
        
    def run(self, data):
        allocation_dict = {}
        # Short-term and long-term window sizes for SMA
        short_window = 20
        long_window = 50
        
        for ticker in self.tickers:
            short_sma = SMA(ticker, data["ohlcv"], length=short_window)
            long_sma = SMA(ticker, data["ohlcv"], length=long_window)
            
            if len(short_sma) == 0 or len(long_sma) == 0:
                log(f"No data for SMA calculation for {ticker}")
                continue
            
            # Check if the short-term SMA is above the long-term SMA
            if short_sma[-1] > long_sma[-1]:
                # Consider bullish trend, allocate a fraction of the portfolio
                allocation_dict[ticker] = 1.0 / len(self.tickers)
                log(f"Buying {ticker}")
            else:
                # Consider bearish trend, do not allocate
                allocation_dict[ticker] = 0
                log(f"Selling {ticker}")
                
            # Allocation dict updates for each ticker based on SMA crossover strategy
                
        return TargetAllocation(allocation_dict)