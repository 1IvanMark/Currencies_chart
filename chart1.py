import plotly.graph_objects as go
import streamlit as st

class ChartCreator:
    def create_currency_chart(self, history):
        if history.empty:
            return go.Figure()

        # Here you can change HUF / currency
        history = history.copy()
        history["HUF_per_currency"] = 1 / history["price"]

        fig = go.Figure()
        colors = {
            "EUR": "green",
            "USD": "red",
            "AUD": "cyan",
            "GBP": "blue",
            "PLN": "orange"
        }

        for currency, group in history.groupby("name"):
            fig.add_trace(go.Scatter(
                x=group["time"],
                y=group["HUF_per_currency"],
                mode="lines+markers",
                name=f"{currency} to HUF",
                line=dict(color=colors.get(currency, "gray"), width=2),
                marker=dict(size=6)
            ))

        fig.update_layout(
            title="Live Currency Rates vs HUF",
            xaxis_title="Time",
            yaxis_title="HUF per unit currency",
            yaxis=dict(range=[50, 550]),  # I used fix range, but it can be changable
            template="plotly_dark",
            height=500
        )

        return fig

    def create_summary_metrics(self, currency_data):
        if not currency_data.empty:
            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    label="Currencies Tracked",
                    value=len(currency_data),
                    delta=None
                )

            with col2:
                last_update = currency_data['time'].max().strftime("%H:%M:%S")
                st.metric(
                    label="Last Update",
                    value=last_update,
                    delta=None
                )
