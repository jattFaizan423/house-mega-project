import streamlit as st

# ------------------- Page Configuration -------------------
st.set_page_config(
    page_title="Gurgaon Real Estate Analytics",
    page_icon="🏘️",
    layout="wide"
)

# ------------------- Initialize session state -------------------
if "page" not in st.session_state:
    st.session_state.page = "home"  # default page

# ------------------- Pages -------------------
def home_page():
    st.title("🏡 Welcome to Gurgaon Real Estate App")
    st.markdown("""
    Discover the Gurgaon real estate market like never before!  
    This app helps you **analyze properties**, **predict prices**, and **get personalized recommendations**.
    """)
    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 💰 Price Prediction")
        st.image("https://img.icons8.com/color/96/000000/money.png", width=80)
        st.markdown("Enter key property details and get an estimated price range in seconds.")

    with col2:
        st.markdown("### 📊 Analytics & Insights")
        st.image("https://img.icons8.com/color/96/000000/combo-chart.png", width=80)
        st.markdown("Explore sector trends, price distributions, BHK statistics, and interactive maps.")

    with col3:
        st.markdown("### 🏘️ Recommendation System")
        st.image("https://img.icons8.com/color/96/000000/home.png", width=80)
        st.markdown("Find top properties in your preferred location and get personalized recommendations.")


def price_prediction_page():
    st.title("💰 House Price Prediction")
    st.write("Your House Price Prediction content here.")


def analysis_page():
    st.title("📊 Analytics & Insights")
    st.write("Your Analytics content here.")


def recommendation_page():
    st.title("🏘️ Recommendation System")
    st.write("Your Recommendation System content here.")


# ------------------- Sidebar Navigation -------------------
st.sidebar.title("Navigation")

if st.sidebar.button("🏡 Home"):
    st.session_state.page = "home"

if st.sidebar.button("💰 Price Prediction"):
    st.session_state.page = "price_prediction"

if st.sidebar.button("📊 Analytics"):
    st.session_state.page = "analysis"

if st.sidebar.button("🏘️ Recommendations"):
    st.session_state.page = "recommendation_system"


# ------------------- Page Router -------------------
page_router = {
    "home": home_page,
    "price_prediction": price_prediction_page,
    "analysis": analysis_page,
    "recommendation_system": recommendation_page
}

# ------------------- Render current page safely -------------------
page_router.get(st.session_state.page, home_page)()
