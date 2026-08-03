import yfinance as yf

def fetch_company_info(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    return {
        "name": info.get("longName", "N/A"),
        "sector": info.get("sector", "N/A"),
        "industry": info.get("industry", "N/A"),
        "market_cap": info.get("marketCap", "N/A"),
        "pe_ratio": info.get("trailingPE", "N/A"),
        "dividend_yield": info.get("dividendYield", "N/A")
    }

