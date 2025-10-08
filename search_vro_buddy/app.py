import streamlit as st
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ---------- SETUP ----------
st.set_page_config(page_title="VRO Buddy - Search-First AI", layout="wide")

# ---------- LOAD MODEL ----------
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()

# ---------- SAMPLE PRODUCT CATALOG ----------
@st.cache_data
def load_catalog():
    data = [
        ["Blue Sneakers", "Comfortable running shoes", "Footwear", 4999, "https://images.unsplash.com/photo-1606813909353-9d35f4b4f59b"],
        ["Red Heels", "Stylish heels for party wear", "Footwear", 2999, "https://images.unsplash.com/photo-1606814725696-9d35f4b4f59b"],
        ["Black Leather Jacket", "Trendy biker jacket", "Clothing", 7999, "https://images.unsplash.com/photo-1618354691438-2f8e62dc2b16"],
        ["White T-Shirt", "Soft cotton casual tee", "Clothing", 999, "https://images.unsplash.com/photo-1520975918318-7b11f5eb6e2d"],
        ["Smart Watch", "Fitness tracker with notifications", "Accessories", 5999, "https://images.unsplash.com/photo-1511739001486-6bfe10ce785f"],
        ["Sunglasses", "UV protected stylish glasses", "Accessories", 1999, "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c"],
        ["Denim Jeans", "Regular fit stretch jeans", "Clothing", 2499, "https://images.unsplash.com/photo-1582738412146-29fffa9f41d4"],
        ["Running Shoes", "Lightweight and durable shoes", "Footwear", 3499, "https://images.unsplash.com/photo-1599058917212-d750089bc07d"],
        ["Leather Handbag", "Elegant brown handbag", "Accessories", 4499, "https://images.unsplash.com/photo-1541099649105-f69ad21f3246"],
        ["Formal Shirt", "Office wear plain shirt", "Clothing", 1799, "https://images.unsplash.com/photo-1585157603015-71c7a0d9c5b5"]
    ]
    df = pd.DataFrame(data, columns=["Name", "Description", "Category", "Price", "Image"])
    df["Embedding"] = list(model.encode(df["Name"] + " " + df["Description"], show_progress_bar=False))
    return df

catalog = load_catalog()

# ---------- SEARCH FUNCTION ----------
def search_products(query, price_range=None, category=None, top_k=5):
    if not query:
        return catalog.sample(top_k)
    
    query_emb = model.encode([query])
    catalog["Similarity"] = cosine_similarity(list(catalog["Embedding"]), query_emb).flatten()

    results = catalog.copy()
    if price_range:
        results = results[(results["Price"] >= price_range[0]) & (results["Price"] <= price_range[1])]
    if category and category != "All":
        results = results[results["Category"] == category]
    
    results = results.sort_values(by="Similarity", ascending=False)
    return results.head(top_k)

# ---------- SIDEBAR ----------
st.sidebar.header("Search Filters")
query = st.sidebar.text_input("Enter your search query:", "blue sneakers under 5000")
category = st.sidebar.selectbox("Category", ["All"] + sorted(catalog["Category"].unique().tolist()))
price_range = st.sidebar.slider("Price Range (₹)", 500, 10000, (500, 8000), step=500)

# ---------- MAIN SECTION ----------
st.title("🛍️ VRO Buddy – Your Search-First AI Shopping Companion")
st.markdown("Type your query and discover products instantly using **AI-powered search.**")

results = search_products(query, price_range, category)

# ---------- DISPLAY RESULTS ----------
cols = st.columns(3)
for i, (_, row) in enumerate(results.iterrows()):
    with cols[i % 3]:
        st.image(row["Image"], use_container_width=True)
        st.subheader(row["Name"])
        st.caption(row["Description"])
        st.write(f"**Category:** {row['Category']}")
        st.write(f"💰 **₹{row['Price']}**")
        if st.button(f"❤️ Like {row['Name']}", key=row["Name"]):
            st.session_state.setdefault("liked_items", []).append(row["Name"])
            st.success(f"Added {row['Name']} to your liked items!")

# ---------- PERSONALIZATION (Optional) ----------
if "liked_items" in st.session_state and len(st.session_state["liked_items"]) > 0:
    st.markdown("---")
    st.subheader("⭐ Your Liked Items")
    liked = catalog[catalog["Name"].isin(st.session_state["liked_items"])]
    for _, item in liked.iterrows():
        st.write(f"- {item['Name']} ({item['Category']}, ₹{item['Price']})")

# ---------- FOOTER ----------
st.markdown("---")
st.caption("Developed as part of Project 2: Search-First VRO Buddy | Streamlit Prototype")
st.markdown("""
    <div style='text-align: center;'>
        <p>Developed with ❤️ using Streamlit</p>
        <p>© 2025 Prerna Gyanchandani.</p>
    </div>
    """, unsafe_allow_html=True)
