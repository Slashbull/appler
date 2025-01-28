import streamlit as st
from submodules.key_metrics import calculate_kpis
from submodules.trends_tools import get_monthly_trends, get_yearly_trends, get_comparative_trends
from submodules.state_visuals import plot_state_contributions, plot_state_heatmap
from submodules.contribution_tools import plot_contributions
from submodules.anomaly_detection import detect_anomalies
from submodules.report_generator import generate_pdf_report, download_csv
from submodules.growth_metrics import calculate_growth_metrics
from submodules.smart_alerts import get_smart_alerts
from submodules.ml_forecasting import forecast_imports
from core import get_filtered_data

def run(data):
    st.title("📊 Market Overview Dashboard")
    st.markdown("Analyze your imports with insights into key metrics, trends, and contributions.")

    # Sidebar Filters
    st.sidebar.header("Filters")
    state = st.sidebar.selectbox("State", options=["All"] + sorted(data['State'].unique().tolist()))
    month = st.sidebar.selectbox("Month", options=["All"] + sorted(data['Month'].unique().tolist()))
    year = st.sidebar.selectbox("Year", options=["All"] + sorted(data['Year'].unique().tolist()))
    importer = st.sidebar.selectbox("Importer", options=["All"] + sorted(data['Consignee Name'].unique().tolist()))
    exporter = st.sidebar.selectbox("Exporter", options=["All"] + sorted(data['Exporter Name'].unique().tolist()))

    # Filter Data
    filtered_data = get_filtered_data(data, state=state, month=month, year=year, importer=importer, exporter=exporter)
    if filtered_data.empty:
        st.warning("No data available for the selected filters.")
        return

    # Tabs for insights
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📌 Key Metrics",
        "📈 Trends",
        "🌍 State Contributions",
        "👥 Importer/Exporter Contributions",
        "🚨 Smart Alerts",
        "🔮 AI Forecasting",
    ])

    # Tab 1: Key Metrics
    with tab1:
        st.subheader("📌 Key Metrics")
        try:
            metrics = calculate_kpis(filtered_data)
            growth_metrics = calculate_growth_metrics(filtered_data)

            # Display metrics
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Imports (Kgs)", f"{metrics['total_imports']:,.0f}")
            col2.metric("Total Shipments", f"{metrics['total_shipments']}")
            col3.metric("YoY Growth", f"{growth_metrics['yoy_growth']:.2f}%", delta_color="normal")
            st.metric("MoM Growth", f"{growth_metrics['mom_growth']:.2f}%")
            st.metric("Top Importer", metrics['top_importer'])
            st.metric("Top Exporter", metrics['top_exporter'])
        except Exception as e:
            st.error(f"Error processing Key Metrics: {e}")

    # Tab 2: Trends
    with tab2:
        st.subheader("📈 Trends Over Time")
        try:
            monthly_trends_chart = get_monthly_trends(filtered_data)
            yearly_trends_chart = get_yearly_trends(filtered_data)
            comparison_chart = get_comparative_trends(filtered_data, comparison_column="Year")
            st.plotly_chart(monthly_trends_chart, use_container_width=True)
            st.plotly_chart(yearly_trends_chart, use_container_width=True)
            st.plotly_chart(comparison_chart, use_container_width=True)
        except Exception as e:
            st.error(f"Error processing Trends: {e}")

    # Tab 3: State Contributions
    with tab3:
        st.subheader("🌍 State Contributions")
        try:
            state_chart = plot_state_contributions(filtered_data)
            st.plotly_chart(state_chart, use_container_width=True)

            st.markdown("### State Heatmap")
            state_heatmap = plot_state_heatmap(filtered_data)
            st.plotly_chart(state_heatmap, use_container_width=True)
        except Exception as e:
            st.error(f"Error processing State Contributions: {e}")

    # Tab 4: Importer/Exporter Contributions
    with tab4:
        st.subheader("👥 Importer/Exporter Contributions")
        try:
            st.markdown("### Top Importers")
            importer_chart = plot_contributions(filtered_data, 'Consignee Name')
            st.plotly_chart(importer_chart, use_container_width=True)

            st.markdown("### Top Exporters")
            exporter_chart = plot_contributions(filtered_data, 'Exporter Name')
            st.plotly_chart(exporter_chart, use_container_width=True)
        except Exception as e:
            st.error(f"Error processing Importer/Exporter Contributions: {e}")

    # Tab 5: Smart Alerts
    with tab5:
        st.subheader("🚨 Smart Alerts")
        try:
            alerts = get_smart_alerts(filtered_data)
            if alerts:
                for alert in alerts:
                    st.warning(alert)
            else:
                st.success("No critical alerts!")
        except Exception as e:
            st.error(f"Error processing Smart Alerts: {e}")

    # Tab 6: AI Forecasting
    with tab6:
        st.subheader("🔮 AI Forecasting")
        try:
            forecast_chart = forecast_imports(filtered_data)
            st.plotly_chart(forecast_chart, use_container_width=True)
        except Exception as e:
            st.error(f"Error processing AI Forecasting: {e}")

    # Exportable Reports
    st.sidebar.title("📄 Exportable Reports")
    try:
        if st.sidebar.button("Generate PDF Report"):
            report_path = generate_pdf_report(filtered_data, metrics)
            st.success("Report generated successfully!")
            st.markdown(f"[Download PDF Report]({report_path})")
    except Exception as e:
        st.error(f"Error generating PDF report: {e}")

    try:
        csv_data = download_csv(filtered_data)
        st.sidebar.download_button("Download CSV", csv_data, "filtered_data.csv", mime="text/csv")
    except Exception as e:
        st.error(f"Error downloading CSV: {e}")
