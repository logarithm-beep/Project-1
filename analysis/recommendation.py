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

    # Final recommendation
    if score >= 4:
        signal = "BUY"

    elif score <= -4:
        signal = "SELL"

    else:
        signal = "HOLD"

    return {
        "Signal": signal,
        "Score": score,
        "Reasons": reasons
    }