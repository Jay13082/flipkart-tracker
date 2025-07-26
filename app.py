# app.py

import streamlit as st
from scraper import scrape_flipkart
from categories import CATEGORIES
import pandas as pd

st.set_page_config(page_title="Flipkart Product Tracker", layout="wide")
st.title("🛒 Flipkart New Listings Tracker")

col1, col2 = st.columns([2, 1])
with col1:
    query = st.text_input("🔍 Enter Product Name (optional)", "")

with col2:
    selected_category = st.selectbox("📂 Or Choose from Categories", [""] + list(CATEGORIES.keys()))

st.markdown("### Filter:")
time_filter = st.radio("Show listings from:", ["Show All", "Today Only", "This Month"], horizontal=True)

if st.button("🚀 Fetch Listings"):
    if query:
        search_url = f"https://www.flipkart.com/search?q={query.replace(' ', '+')}&sort=recency_desc"
    elif selected_category:
        search_url = CATEGORIES[selected_category] + "&sort=recency_desc"
    else:
        st.warning("Please enter a search term or select a category.")
        st.stop()

    with st.spinner("Scraping Flipkart... Please wait"):
        data = scrape_flipkart(search_url)

    if not data:
        st.error("No products found.")
    else:
        st.success(f"Found {len(data)} products!")

        for product in data:
            with st.container():
                c1, c2 = st.columns([1, 3])
                with c1:
                    st.image(product['image'], width=120)
                with c2:
                    st.markdown(f"**{product['title']}**")
                    st.markdown(f"💰 {product['price']}")
                    st.markdown(f"[View on Flipkart]({product['link']})", unsafe_allow_html=True)

        df = pd.DataFrame(data)
        st.download_button("⬇️ Download CSV", df.to_csv(index=False), file_name="flipkart_products.csv", mime="text/csv")
