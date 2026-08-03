import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


def plot_price_chart(df,ticker,show_ma20,show_ma50,show_ma100):
    fig = make_subplots(
          rows = 2,
          cols = 1,
          shared_xaxes= True,
          vertical_spacing= 0.05,
          row_heights=[0.7,0.3]
    )

    fig.add_trace(
        go.Candlestick(
            x = df.index,
            open = df["Open"],
            close = df["Close"],
            high = df["High"],
            low = df["Low"],
            name = "Candlestick"
        ),
        row = 1,
        col = 1
    )
    if show_ma20:
        fig.add_trace(
            go.Scatter(
                    x = df.index,
                    y = df[f"MA20"],
                    mode = "lines",
                    name = f"Moving average 20"
                ),
                row = 1,
                col = 1
        )

    if show_ma50:
            fig.add_trace(
                go.Scatter(
                        x = df.index,
                        y = df[f"MA50"],
                        mode = "lines",
                        name = f"Moving average 50"
                    ),
                    row = 1,
                    col = 1
            )

    if show_ma100:
            fig.add_trace(
                go.Scatter(
                        x = df.index,
                        y = df[f"MA100"],
                        mode = "lines",
                        name = f"Moving average 100"
                    ),
                    row = 1,
                    col = 1
            )
    colors = np.where(
      df["Close"] >= df["Open"],
      "green",
      "red"
    )
    fig.add_trace(
          go.Bar(
                x = df.index,
                y = df["Volume"],
                name = "Volume",
                marker_color = colors
          ),
          row = 2,
          col = 1
    )

    fig.update_layout(
        height = 650,
        xaxis_rangeslider_visible = False,
        title = f"{ticker} Stock Analysis",
        template="plotly_dark"
    )
    fig.update_yaxes(
          showgrid=False,
          title_text="Price",
          row=1,
          col=1
    )
    fig.update_yaxes(
            showgrid=False,
            title_text="Volume",
            row=2,
            col=1
        )
    fig.update_xaxes(
          title_text = "Date",
          row=2,
          col=1
    )

    return fig