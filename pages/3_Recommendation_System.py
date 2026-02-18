import streamlit as st
import pickle
import pandas as pd
import numpy as np

# ------------------------------
# Page Setup
# ------------------------------
st.set_page_config(
    page_title="🏙️ Recommendation System",
    layout="wide",
    page_icon="🏘️"
)

st.title("🏘️ Recommendation System")
st.markdown("---")

# ------------------------------
# Load Data (Cached)
# ------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("appartments.csv")
    important_cols = [
        "PropertyName", "PropertySubName", "Link",
        "PriceDetails", "TopFacilities",
        "NearbyLocations", "LocationAdvantages"
    ]
    df = df[important_cols]
    df['PropertyName'] = df['PropertyName'].str.strip()

    location_df = pickle.load(open('location_distance.pkl', 'rb'))
    cosine_sim1 = pickle.load(open('cosine_sim1.pkl', 'rb'))
    cosine_sim2 = pickle.load(open('cosine_sim2.pkl', 'rb'))
    cosine_sim3 = pickle.load(open('cosine_sim3.pkl', 'rb'))

    location_df.index = location_df.index.str.strip()

    cosine_sim_matrix = 0.5 * cosine_sim1 + 0.8 * cosine_sim2 + 1.0 * cosine_sim3

    return df, location_df, cosine_sim_matrix

df, location_df, cosine_sim_matrix = load_data()

# ------------------------------
# Recommendation Function
# ------------------------------
def recommend_properties(property_name, top_n=5):

    if property_name not in location_df.index:
        st.error(f"Property '{property_name}' not found!")
        return pd.DataFrame()

    idx = location_df.index.get_loc(property_name)
    sim_scores = list(enumerate(cosine_sim_matrix[idx]))
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    top_indices = [i[0] for i in sorted_scores[1:top_n + 1]]
    top_properties = location_df.index[top_indices].tolist()

    rec_df = pd.DataFrame({
        "PropertyName": top_properties
    })

    return rec_df

# ------------------------------
# Location + Radius Input
# ------------------------------
col1, col2 = st.columns([2, 1])

with col1:
    selected_location = st.selectbox(
        "📍 Select a Location",
        sorted(location_df.columns)
    )

with col2:
    radius = st.number_input(
        "🧭 Radius (km)",
        min_value=0.1,
        step=0.1
    )

# ------------------------------
# Session State
# ------------------------------
if "nearby_properties" not in st.session_state:
    st.session_state.nearby_properties = []

# ------------------------------
# Search Button
# ------------------------------
if st.button("🔍 Search Nearby Properties"):

    nearby_ser = location_df[
        location_df[selected_location].dropna() < radius * 1000
    ][selected_location].sort_values()

    st.session_state.nearby_properties = nearby_ser.index.tolist()

    if len(st.session_state.nearby_properties) == 0:
        st.warning("No properties found in this radius.")

# ------------------------------
# Display Nearby Properties
# ------------------------------
if st.session_state.nearby_properties:

    st.success(
        f"Found {len(st.session_state.nearby_properties)} properties within {radius} km of {selected_location}"
    )

    for prop in st.session_state.nearby_properties:
        distance = location_df.loc[prop, selected_location] / 1000
        st.markdown(f"✅ **{prop}** — {round(distance, 2)} km")

    selected_property = st.selectbox(
        "🏢 Choose a property to view recommendations",
        st.session_state.nearby_properties
    )

    # ------------------------------
    # Recommendations
    # ------------------------------
    recommendations = recommend_properties(selected_property)

    if not recommendations.empty:
        st.markdown("### 🌟 Top Recommended Properties")

        recommendations_display = recommendations.copy()
        recommendations_display.insert(
            0, "Rank", range(1, len(recommendations_display) + 1)
        )

        st.dataframe(recommendations_display, use_container_width=True)
















