import streamlit as st
from data.fetch_data import fetch_stock_data 
from ui.charts import plot_price_chart
from indicators.moving_average import calculate_ma
from data.company_info import fetch_company_info
from utils.formatters import format_large_number
from indicators.rsi import calculate_rsi
from indicators.macd import calculate_macd
from indicators.bollinger_band import bollinger_band
from indicators.adx import calculate_adx
from analysis.recommendation import generate_recommendation, calculate_volume

st.title("SmartStocks AI")
st.write("Welcome to SmartStocks AI")
st.sidebar.title("📊 SmartStocks AI")
st.sidebar.subheader("Indicators:")

show_ma20 = st.sidebar.checkbox("MA20")
show_ma50 = st.sidebar.checkbox("MA50")
show_ma100 = st.sidebar.checkbox("MA100")
show_bollinger = st.sidebar.checkbox("Bollinger Bands")
show_adx = st.sidebar.checkbox("ADX")

st.sidebar.divider()

ticker = st.text_input("Enter Stock Ticker: ")
time_period = st.selectbox("Select time period",
                           options=["1d", "5d", "1mo", "6mo", "1y", "5y", "max"],
                           index = 4)

if st.button("Fetch Data"):
    try:
        df,actual_ticker = fetch_stock_data(ticker.upper(),period=time_period)
        company_info = fetch_company_info(actual_ticker)
        current_price = df["Close"].iloc[-1]
        Previous_price =df["Close"].iloc[-2]
        price_change = current_price-Previous_price
        percentage_change = (price_change/Previous_price)*100
       
                
        if show_ma20:
            df = calculate_ma(df, 20)

        if show_ma50:
            df = calculate_ma(df, 50)

        if show_ma100:
            df = calculate_ma(df, 100)
        if "MA50" not in df.columns:
            df = calculate_ma(df, 50)

        

        df = calculate_rsi(df,14)
        df = calculate_macd(df)
        df = bollinger_band(df)
        df = calculate_volume(df)
        df = calculate_adx(df)

        result = generate_recommendation(df)
       

        fig = plot_price_chart(df,actual_ticker,show_ma20,show_ma50,show_ma100,show_bollinger,show_adx)

        st.subheader(company_info["name"])
        col1, col2,col3 = st.columns(3)

        with col1:
            st.write(f"**Sector:** {company_info['sector']}")

        with col2:
            st.write(f"**Industry:** {company_info['industry']}")

        with col3:
            st.write(f"**Market Cap:** {format_large_number(company_info['market_cap'])}")

        st.subheader("AI Recommendation")
        signal = result["Signal"]
        score = result["Score"]
        reasons = result["Reasons"]

        if signal == "BUY":
            st.success(f"🟢 BUY — Score: {score}")

        elif signal == "SELL":
            st.error(f"🔴 SELL — Score: {score}")

        else:
            st.warning(f"🟡 HOLD — Score: {score}")

        st.write("### Why?")

        for reason in reasons:
            st.write(f"• {reason}")


        col1,col2,col3,col4 = st.columns(4)
        st.success(f"Using ticker: {actual_ticker}")
        with col1:
            st.metric(
                label="📈 Current Price",
                value = f"₹{current_price:.2f}",
                delta= f"{price_change:+.2f} ({percentage_change:+.2f})%"
            )
        with col2:
            st.metric(
                label="📊 Today's Volume",
                value=f"{format_large_number(df['Volume'].iloc[-1])}"
            )
        with col3:
            st.metric(
                label="⬆️ 52 Week High",
                value=f"₹{df['High'].max():.2f}"
                )
        with col4:
            st.metric(
                label="⬇️52 Week Low",
                value=f"₹{df['Low'].min():.2f}"
            )
        st.write(df.tail())
        st.plotly_chart(fig)
    except ValueError as e:
        st.error(str(e))

