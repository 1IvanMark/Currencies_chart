import streamlit as st
import time
from datetime import datetime
from data_source1 import DataSource
from chart1 import ChartCreator
import pandas as pd

st.set_page_config(
    page_title="Currency Dashboard",
    page_icon="💱",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("💱 Live Currency Rates vs HUF")
    st.markdown("Visualize real-time currency rates!")

    st.sidebar.header("Settings")
    auto_refresh = st.sidebar.checkbox("Enable Auto Refresh", value=True)
    refresh_interval = st.sidebar.slider("Update every (seconds)", 5, 50, 10)

    st.sidebar.markdown("### Currencies:")
    st.sidebar.write("Tracking USD, EUR, GBP, AUD, PLN")

    data_source = DataSource()
    chart_creator = ChartCreator()

    status_container = st.empty()
    metrics_container = st.empty()
    chart_container = st.empty()

    update_count = 0
    history = pd.DataFrame()

    while auto_refresh:
        update_count += 1
        with status_container.container():
            st.info(f"🔄 Updating data... (Update #{update_count})")

        currency_data = data_source.get_currency_rates()
        if not currency_data.empty:
            currency_data['update_id'] = update_count
            history = pd.concat([history, currency_data], ignore_index=True)

        with metrics_container.container():
            chart_creator.create_summary_metrics(currency_data)

        with chart_container.container():
            if not history.empty:
                currency_chart = chart_creator.create_currency_chart(history)
                st.plotly_chart(currency_chart, use_container_width=True)

                with st.expander("📊 View Raw Data"):
                    st.dataframe(history[['name','price','time']])
            else:
                st.warning("⚠️ Could not fetch currency data.")

        st.markdown(f"**Next update in:** {refresh_interval} seconds")
        time.sleep(refresh_interval)

if __name__ == "__main__":
    main()
