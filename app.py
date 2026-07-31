import streamlit as st
from data.fetch_data import fetch_stock_data 

st.title("SmartStocks AI")
st.write("Welcome to SmartStocks AI")

ticker = st.text_input("Enter Stock Ticker")

if st.button("Fetch Data"):
    try:
        df,actual_ticker = fetch_stock_data(ticker.upper())
        # st.write(df.tail())
        print(df.tail())
        
        st.success(f"Using ticker: {actual_ticker}")
        # st.dataframe(df)
    except ValueError as e:
        st.error(str(e))

