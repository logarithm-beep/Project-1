def bollinger_band(df):
    df["MA20"] = df["Close"].rolling(window = 20).mean()
    df["STD20"] = df["Close"].rolling(window=20).std()
    df["Upper"] = df["MA20"] + 2*(df["STD20"])
    df["Lower"] = df["MA20"] - 2*(df["STD20"])
    return df