import streamlit as st

st.set_page_config(page_title="Semantic Layer", layout="wide")

st.title("🔍 Semantic Layer Explorer")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Query Builder")
    metrics = st.multiselect("Select Metrics", ["total_users", "revenue"])
    dimensions = st.multiselect("Select Dimensions", ["country", "date"])

with col2:
    st.subheader("Results")
    if st.button("Execute Query"):
        st.write("Query results will appear here")
