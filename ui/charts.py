import plotly.graph_objects as go
from indicators.moving_average import calculate_ma

def plot_price_chart(df,ticker,show_ma20,show_ma50,show_ma100):
    fig = go.Figure()

    fig.add_trace(
        go.Candlestick(
            x = df.index,
            open = df["Open"],
            close = df["Close"],
            high = df["High"],
            low = df["Low"],
            name = "Candlestick"
        )
    )
    if show_ma20:
        period = 20
        fig.add_trace(
            go.Scatter(
                    x = df.index,
                    y = df[f"MA20"],
                    mode = "lines",
                    name = f"Moving average 20"
                )
        )

    if show_ma50:
            period = 50
            fig.add_trace(
                go.Scatter(
                        x = df.index,
                        y = df[f"MA50"],
                        mode = "lines",
                        name = f"Moving average 50"
                    )
            )

    if show_ma100:
            period = 100
            fig.add_trace(
                go.Scatter(
                        x = df.index,
                        y = df[f"MA100"],
                        mode = "lines",
                        name = f"Moving average 100"
                    )
            )

    fig.update_layout(
        title = f"{ticker} Stock Price",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_white"
    )

    return fig