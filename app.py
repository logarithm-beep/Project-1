import streamlit as st
import pandas as pd  
import yfinance as yf
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
stocks = pd.read_csv("stocks.csv")

stocks['Display'] = (stocks["SYMBOL"] + ' - ' + stocks["NAME OF COMPANY"] )

st.sidebar.divider()

search = st.text_input(
    "🔎 Search Stock",
    placeholder="Enter ticker or company name...")
if search:

    search_lower = search.lower()

    matches = stocks[
        stocks["SYMBOL"].str.lower().str.contains(search_lower, na=False)
        |
        stocks["NAME OF COMPANY"].str.lower().str.contains(search_lower, na=False)
    ]

    matches = matches.head(10)

if search and not matches.empty:

    selected_stock = st.selectbox(
        "Select a stock",
        matches["Display"].tolist()
    )

else:
    selected_stock = search.upper()

if " - " in selected_stock:
    ticker = selected_stock.split(" - ")[0]
else:
    ticker = selected_stock
time_period = st.selectbox("Select time period",
                           options=["6mo", "1y", "5y", "max"],
                           index = 1)

if st.button("Fetch Data"):
    try:
        df,actual_ticker = fetch_stock_data(ticker.upper(),period=time_period)
        company_info = fetch_company_info(actual_ticker)
        one_year_data = yf.Ticker(actual_ticker).history(period="1y")
        current_price = df["Close"].iloc[-1]
        Previous_price =df["Close"].iloc[-2]
        price_change = current_price-Previous_price
        percentage_change = (price_change/Previous_price)*100
        stock = yf.Ticker(actual_ticker)
       
                
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

        st.title(company_info["name"])

        with st.expander("ℹ️ Company Information"):

            col1, col2, col3 = st.columns(3)

            with col1:
                st.write(f"**Sector:** {company_info['sector']}")

            with col2:
                st.write(f"**Industry:** {company_info['industry']}")

            with col3:
                st.write(
                    f"**Market Cap:** "
                    f"{format_large_number(company_info['market_cap'])}"
                )

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
                value=f"₹{one_year_data['High'].max():.2f}"
                )
        with col4:
            st.metric(
                label="⬇️52 Week Low",
                value=f"₹{one_year_data['Low'].min():.2f}"
            )
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Overview",
            "📈 Technical",
            "💰 Performance",
            "⚠️ Risk"
        ])

        with tab1:
            st.subheader("🤖 AI Recommendation")
            with st.container(border=True):
                signal = result["Signal"]
                score = result["Score"]
                reasons = result["Reasons"]
                Indicator_scores = result["IndicatorScores"]

                if signal == "BUY":
                    st.success(f"🟢 BUY — Score: {score}")

                elif signal == "SELL":
                    st.error(f"🔴 SELL — Score: {score}")

                else:
                    st.warning(f"🟡 HOLD — Score: {score}")

                st.write("### Why?")

                for reason in reasons:
                    st.write(f"✓ {reason}")

                st.write("#### 📊 Score Breakdown")

                cols = st.columns(3)

                for i, (indicator, points) in enumerate(Indicator_scores.items()):

                    with cols[i % 3]:

                        if points > 0:
                            st.success(f"🟢 {indicator}\n+{points}")

                        elif points < 0:
                            st.error(f"🔴 {indicator}\n{points}")

                        else:
                            st.info(f"⚪ {indicator}\n0")

        with tab2:
            st.subheader("📈 Technical Analysis")
            st.plotly_chart(fig, use_container_width=True)
        def calculate_return(df, days):
            if df.empty:
                return None

            current_price = df["Close"].iloc[-1]
            current_date = df["Close"].index[-1]
            
            target_date = current_date - pd.Timedelta(days=days)

            previous_data = df[df.index <= target_date] 
            if previous_data.empty:
                return None

            Previous_price = previous_data["Close"].iloc[-1]

            return ((current_price / Previous_price) - 1) * 100


        return_1d = calculate_return(df, 1)
        return_1w = calculate_return(df, 7)
        return_1m = calculate_return(df, 30)
        return_6m = calculate_return(df, 180)
        return_1y = calculate_return(df, 365)
        with tab3:
            st.subheader("💰 Performance")
            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                if return_1d is not None:
                    st.metric("1D", f"{return_1d:+.2f}%")
                else:
                    st.metric("1D", "N/A")

            with col2:
                if return_1w is not None:
                    st.metric("1W", f"{return_1w:+.2f}%")
                else:
                    st.metric("1W", "N/A")

            with col3:
                if return_1m is not None:
                    st.metric("1M", f"{return_1m:+.2f}%")
                else:
                    st.metric("1M", "N/A")
            with col4:
                if return_6m is not None:
                    st.metric("6M", f"{return_6m:+.2f}%")
                else:
                    st.metric("6M", "N/A")

            with col5:
                if return_1y is not None:
                    st.metric("1Y", f"{return_1y:+.2f}%")
                else:
                    st.metric("1Y", "N/A")

        daily_returns = df["Close"].pct_change()
        annual_volatility = (daily_returns.std() * (252 ** 0.5) * 100)        

        rolling_peak = df["Close"].cummax()

        drawdown = ((df["Close"] - rolling_peak)/rolling_peak)
        max_drawdown = drawdown.min() * 100

        with tab4:
            st.subheader("⚠️ Risk")
        
            st.metric(
                "Annualized Volatility",
                f"{annual_volatility:.2f}%")
            st.caption(f"Calculated using {time_period} of historical data.")
            st.metric(
                "Maximum Drawdown",
                f"{max_drawdown:.2f}%")
            st.caption("Maximum drawdown is the largest peak-to-trough decline during the selected period.")
    except ValueError as e:
        st.error(str(e))