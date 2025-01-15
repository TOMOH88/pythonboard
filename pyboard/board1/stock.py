import yfinance as yf

# 특정 주식의 데이터를 가져오기 (예: 애플)
stock = yf.Ticker("AAPL")

# 주식의 기본 정보
print(stock.info)

# 최근 5년간 일간 데이터
historical_data = stock.history(period="5y")
print(historical_data)