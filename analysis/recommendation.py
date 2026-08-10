def calculate_volume(df):
    df["Volume_MA20"] = df["Volume"].rolling(window=20).mean()
    return df

def generate_recommendation(df):
    latest = df.iloc[-1]

    score = 0
    reasons = []

    # RSI
    if latest["RSI"] < 30:
        score += 2
        reasons.append("RSI indicates oversold conditions")

    elif latest["RSI"] > 70:
        score -= 2
        reasons.append("RSI indicates overbought conditions")

    # MACD
    if latest["MACD"] > latest["Signal"]:
        score += 2
        reasons.append("MACD is above signal line")

    elif latest["MACD"] < latest["Signal"]:
        score -= 2
        reasons.append("MACD is below the signal line")

    # MA50
    if latest["Close"] > latest["MA50"]:
        score += 2
        reasons.append("Price is above the 50-day moving average")

    elif latest["Close"] < latest["MA50"]:
        score -= 2
        reasons.append("Price is below the 50-day moving average")
     
    # Bollinger Band and 
    if latest["close"] < latest["Lower"]:
        score += 2
        reasons.append("Price is below the lower bollinger band")

    elif latest["close"] > latest["Higher"]:
        score -= 2
        reasons.append("Price is above the higher bollinger band")

    # Volume
    if latest["Volume"] > latest["Volume_MA20"]:
        if latest["close"] > latest["Open"]:
            score += 1
            reasons.append("Volume confirms bullish price movement")
    
        elif latest["close"] < latest["Open"]:
            score -= 1
            reasons.append("High volume confirms bearish price movement")
        
    
    # Final recommendation
    if score >= 7:
        signal = "Strongly Buy"

    elif score <= -7:
        signal = "Strongly Sell"

    elif score >= 4:
        signal = "Buy"
    elif score <= -4:
        signal = "Sell"
    else:
        signal = "HOLD"

    return {
        "Signal": signal,
        "Score": score,
        "Reasons": reasons
    }