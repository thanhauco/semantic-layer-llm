import streamlit as st
import pandas as pd

def render_chart(data: pd.DataFrame, chart_type: str = "bar"):
    if chart_type == "bar":
        st.bar_chart(data)
    elif chart_type == "line":
        st.line_chart(data)
    else:
        st.dataframe(data)
