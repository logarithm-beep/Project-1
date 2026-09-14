# 📊 SmartStocks AI

SmartStocks AI is a Python-based stock analysis dashboard built with Streamlit.

It allows users to search for stocks, visualize historical price data, analyze technical indicators, evaluate historical performance, and understand basic risk metrics through an interactive dashboard.

## 🚀 Features

- 🔎 Stock search by ticker or company name
- 🇮🇳 Automatic NSE/BSE ticker resolution
- 🕯️ Interactive candlestick charts
- 📈 Moving Averages — MA20, MA50, MA100
- 📊 Volume analysis
- 📉 RSI
- 📈 MACD
- 📏 Bollinger Bands
- 📐 ADX with +DI and -DI
- 🤖 Rule-based technical trading signal
- 📊 Indicator score breakdown
- 💰 Historical performance — 1D, 1W, 1M, 6M, 1Y
- 📈 ₹10,000 normalized performance chart
- ⚠️ Annualized volatility
- 📉 Maximum drawdown
- 🏢 Basic company information

## 🛠️ Tech Stack

- Python
- Streamlit
- Pandas
- NumPy
- yfinance
- Plotly

## 📁 Project Structure

```text
SmartStockAI/
│
├── app.py
├── requirements.txt
├── stocks.csv
│
├── data/
│   ├── fetch_data.py
│   └── company_info.py
│
├── indicators/
│   ├── moving_average.py
│   ├── rsi.py
│   ├── macd.py
│   ├── bollinger_band.py
│   └── adx.py
│
├── analysis/
│   └── recommendation.py
│
├── ui/
│   └── charts.py
│
└── utils/
    └── formatters.py
