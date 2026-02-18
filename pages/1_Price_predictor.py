import streamlit as st
import pickle
import pandas as pd
import numpy as np
import os

# ------------------- Page Config -------------------
st.set_page_config(
    page_title="House Price Predictor",
    page_icon="🏠",
    layout="centered"
)

st.title("🏡 House Price Prediction App")
st.markdown("Enter property details below to estimate the price range.")
st.divider()

# ------------------- Load Data & Pipeline -------------------
@st.cache_resource
def load_files():
    if not os.path.exists('df (1).pkl') or not os.path.exists('pipeline.pkl'):
        st.error("❌ Required files not found in directory!")
        st.stop()

    with open('df (1).pkl', 'rb') as f:
        df = pickle.load(f)
    with open('pipeline.pkl', 'rb') as f:
        pipeline = pickle.load(f)
    return df, pipeline

df, pipeline = load_files()

# ------------------- User Inputs -------------------
col1, col2 = st.columns(2)

with col1:
    property_type = st.selectbox('Property Type', sorted(df['property_type'].dropna().unique()))
    sector = st.selectbox('Sector', sorted(df['sector'].dropna().unique()))
    bedrooms = st.selectbox('Bedrooms', sorted(df['bedRoom'].dropna().unique()))
    bathroom = st.selectbox('Bathrooms', sorted(df['bathroom'].dropna().unique()))
    balcony = st.selectbox('Balconies', sorted(df['balcony'].dropna().unique()))
    property_age = st.selectbox('Property Age', sorted(df['agePossession'].dropna().unique()))

with col2:
    built_up_area = st.number_input('Built-up Area (sq.ft)', min_value=200.0, max_value=10000.0, value=1000.0, step=10.0)
    servant_room = st.selectbox('Servant Room', [0, 1])
    store_room = st.selectbox('Store Room', [0, 1])
    furnishing_type = st.selectbox('Furnishing Type', sorted(df['furnishing_type'].dropna().unique()))
    luxury_category = st.selectbox('Luxury Category', sorted(df['luxury_category'].dropna().unique()))
    floor_category = st.selectbox('Floor Category', sorted(df['floor_category'].dropna().unique()))

st.divider()

# ------------------- Prediction -------------------
st.subheader("Price Prediction")

if st.button('💰 Predict Price'):
    try:
        # Prepare DataFrame
        input_df = pd.DataFrame([{
            'property_type': property_type,
            'sector': sector,
            'bedRoom': bedrooms,
            'bathroom': bathroom,
            'balcony': balcony,
            'agePossession': property_age,
            'built_up_area': built_up_area,
            'servant room': servant_room,
            'store room': store_room,
            'furnishing_type': furnishing_type,
            'luxury_category': luxury_category,
            'floor_category': floor_category
        }])

        # Reorder columns if pipeline expects specific order
        if hasattr(pipeline, 'feature_names_in_'):
            expected_cols = list(pipeline.feature_names_in_)
            for col in expected_cols:
                if col not in input_df.columns:
                    input_df[col] = 0
            input_df = input_df[expected_cols]

        # Make prediction
        pred = pipeline.predict(input_df)[0]
        price = np.expm1(pred)
        low, high = price * 0.78, price * 1.22

        st.success(f"🏠 Estimated Price Range: ₹ {low:.2f} Cr — ₹ {high:.2f} Cr")

    except Exception as e:
        st.error(f"❌ Prediction failed: {e}")










