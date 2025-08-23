import streamlit as st

def show_metric_explorer(model):
    st.subheader("Available Metrics")
    
    for table in model.tables:
        with st.expander(f"📊 {table.name}"):
            for metric in table.metrics:
                st.write(f"- **{metric.name}**: {metric.description or 'No description'}")
