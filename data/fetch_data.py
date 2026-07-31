import yfinance as yf

def fetch_stock_data(ticker, period = '1y'):
    
    possible_tickers = [
        ticker,
        ticker + ".NS",
        ticker + ".BO"
    ]
    for symbol in possible_tickers:
        try:  
            stock = yf.Ticker(symbol)
            data = stock.history(period = period)

            if not data.empty:
                return data,symbol
        except Exception:
            continue

    raise ValueError(f"No data found for ticker {ticker}.")

if __name__ == "__main__":
    ticker = input("Enter stock Ticker: ")
    try: 
        df,actual_ticker = fetch_stock_data(ticker)
        print(f"Using ticker {actual_ticker}")
        print(df.tail())
    except ValueError as e:
        print(e)