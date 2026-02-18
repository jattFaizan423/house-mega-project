import streamlit as st
import pandas as pd
import pickle
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# ---------------- Page Setup ----------------
st.set_page_config(page_title='House Analysis', layout='wide')
st.title('🏠 Area Analysis')

# ---------------- Load Data ----------------
@st.cache_data
def load_data():
    df = pd.read_csv('data_viz1 (1).csv')
    feature_text = pickle.load(open('feature_text.pkl', 'rb'))
    return df, feature_text

new_df, feature_text = load_data()

# Clean numeric data
new_df['built_up_area'] = pd.to_numeric(new_df['built_up_area'], errors='coerce')
new_df['built_up_area'] = new_df['built_up_area'].fillna(0)

# ---------------- Static Map ----------------
group_df = new_df.groupby('sector', as_index=False)[
    ['price', 'price_per_sqft', 'built_up_area', 'latitude', 'longitude']
].mean()

group_df = group_df.dropna(subset=['latitude', 'longitude'])

fig = px.scatter_mapbox(
    group_df,
    lat="latitude",
    lon="longitude",
    color="price_per_sqft",
    size="built_up_area",
    color_continuous_scale=px.colors.cyclical.IceFire,
    zoom=10,
    mapbox_style="open-street-map",
    text="sector",
    hover_name="sector"
)

fig.update_layout(height=700)
st.plotly_chart(fig, use_container_width=True)

# ---------------- Dropdown ----------------
st.subheader("🏘️ Select a Sector to See Its Key Features")

sectors = ['All Sectors'] + sorted(new_df['sector'].dropna().unique().tolist())
selected_sector = st.selectbox('Choose Sector', sectors)

# ---------------- WordCloud ----------------
st.header(f'🧩 Features in {selected_sector}')

if selected_sector == 'All Sectors':
    df_filtered = new_df
else:
    df_filtered = new_df[new_df['sector'] == selected_sector]

# Get text data
if 'description' in df_filtered.columns:
    text_data = " ".join(df_filtered['description'].dropna().astype(str))
elif 'features' in df_filtered.columns:
    text_data = " ".join(df_filtered['features'].dropna().astype(str))
else:
    text_data = str(feature_text)

# Generate WordCloud
if len(text_data.strip()) == 0:
    st.warning("⚠️ No text data available for this sector.")
else:
    wordcloud = WordCloud(
        width=800,
        height=800,
        background_color='white',
        stopwords=set(['s', 'na', 'none']),
        min_font_size=10
    ).generate(text_data)

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    plt.tight_layout(pad=0)

    st.pyplot(fig)



















