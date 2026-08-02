import streamlit as st
from data.fetch_data import fetch_stock_data 
from ui.charts import plot_price_chart
from indicators.moving_average import calculate_ma

st.title("SmartStocks AI")
st.write("Welcome to SmartStocks AI")
st.sidebar.header("Indicators:")

show_ma20 = st.sidebar.checkbox("MA20")
show_ma50 = st.sidebar.checkbox("MA50")
show_ma100 = st.sidebar.checkbox("MA100")

st.sidebar.divider()

ticker = st.text_input("Enter Stock Ticker: ")

if st.button("Fetch Data"):
    try:
        df,actual_ticker = fetch_stock_data(ticker.upper())
        if show_ma20:
            df = calculate_ma(df, 20)

        if show_ma50:
            df = calculate_ma(df, 50)

        if show_ma100:
            df = calculate_ma(df, 100)

        # df,period = calculate_ma(df,period)
        fig = plot_price_chart(df,actual_ticker,show_ma20,show_ma50,show_ma100)

        st.success(f"Using ticker: {actual_ticker}")
        st.write(df.tail())
        st.plotly_chart(fig)
    except ValueError as e:
        st.error(str(e))

