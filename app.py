import streamlit as st

st.title("SmartStocks AI")
st.write("Welcome to SmartStocks AI")

ticker = st.text_input("Enter Stock Ticker")

st.write("You entered: ",ticker)