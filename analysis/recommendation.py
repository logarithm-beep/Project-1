def calculate_volume(df):
    df["Volume_MA20"] = df["Volume"].rolling(window=20, min_periods=1).mean()
    return df

def generate_recommendation(df):
    if "Volume_MA20" not in df.columns:
        df = calculate_volume(df)
    df = df.dropna(subset=[
        "RSI",
        "MACD",
        "Signal",
        "BB_Width",
        "STD20",
        "MA20",
        "MA50",
        "Lower",
        "Upper",
        "Open",
        "High",
        "Low",
        "Close",
        "Volume"
    ])
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
    if latest["Close"] < latest["Lower"]:
        score += 2
        reasons.append("Price is below the lower bollinger band")

    elif latest["Close"] > latest["Upper"]:
        score -= 2
        reasons.append("Price is above the higher bollinger band")

    # Volume
    if latest["Volume"] > latest["Volume_MA20"]:
        if latest["Close"] > latest["Open"]:
            score += 1
            reasons.append("Volume confirms bullish price movement")
    
        elif latest["Close"] < latest["Open"]:
            score -= 1
            reasons.append("High volume confirms bearish price movement")

        if latest["ADX"] > 25:
            if latest["+DI"] > latest["-DI"]:
                score += 1
                reasons.append("ADX confirms a strong bullish trend")

            elif latest["-DI"] > latest["+DI"]:
                score -= 1
                reasons.append("ADX confirms a strong bearish trend")
        
    
    # Final recommendation
    if score > 6:
        signal = "STRONG BUY"

    elif score > 3:
        signal = "BUY"

    elif score < -6:
        signal = "STRONG SELL"

    elif score < -3:
        signal = "SELL"

    else:
        signal = "HOLD"

    confidence = abs(score)/9 * 100

    return {
        "Signal": signal,
        "Score": score,
        "Confidence": confidence,
        "Reasons": reasons
    }