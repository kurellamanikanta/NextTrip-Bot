from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq

# Load env
load_dotenv()

# Page config
st.set_page_config(
    page_title="NextTrip Bot",
    page_icon="✈️",
    layout="wide"
)

# ---------------- PREMIUM CSS ---------------- #
st.markdown("""
<style>

/* Google Font */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

/* Full App */
html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* Background */
.stApp {
    background: linear-gradient(135deg, #f8fafc, #eef2ff);
    color: #111827;
}

/* Hide Streamlit Branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Main Container */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* ---------- HERO SECTION ---------- */

.hero {
    text-align: center;
    margin-bottom: 2rem;
}

.hero-title {
    font-size: 4rem;
    font-weight: 800;
    background: linear-gradient(90deg, #ff6b00, #ff9500);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: float 3s ease-in-out infinite;
    text-shadow: 0px 6px 20px rgba(255,140,0,0.2);
}

.hero-subtitle {
    font-size: 1.2rem;
    color: #475569;
    margin-top: 10px;
    font-weight: 500;
}

/* Floating animation */
@keyframes float {
    0% {transform: translateY(0px);}
    50% {transform: translateY(-6px);}
    100% {transform: translateY(0px);}
}

/* ---------- CHAT ---------- */

.stChatMessage {
    background: rgba(255,255,255,0.92);
    border-radius: 20px;
    padding: 18px;
    margin-bottom: 18px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 8px 24px rgba(0,0,0,0.06);
}

/* Text Fix */
.stMarkdown,
.stMarkdown p,
.stChatMessage p,
.stChatMessage div {
    color: #111827 !important;
    font-size: 16px;
    line-height: 1.7;
}

/* User Message */
[data-testid="chatAvatarIcon-user"] + div {
    background: linear-gradient(135deg, #fff7ed, #ffedd5);
}

/* Assistant Message */
[data-testid="chatAvatarIcon-assistant"] + div {
    background: white;
}

/* ---------- INPUT ---------- */

.stChatInput input {
    background: white !important;
    color: #111827 !important;
    border-radius: 16px !important;
    border: 1px solid #d1d5db !important;
    padding: 14px !important;
}

/* Placeholder */
.stChatInput input::placeholder {
    color: #6b7280 !important;
}

/* ---------- SIDEBAR ---------- */

section[data-testid="stSidebar"] {
    background: white;
    border-right: 1px solid #e5e7eb;
}

section[data-testid="stSidebar"] * {
    color: #111827 !important;
}

/* Sidebar cards */
[data-testid="stSidebar"] .stAlert {
    background: linear-gradient(135deg, #fff7ed, #ffedd5);
    border-radius: 12px;
    border: none;
}

/* ---------- BUTTONS ---------- */

.stButton button {
    background: linear-gradient(90deg, #ff6b00, #ff9500);
    color: white !important;
    border: none;
    border-radius: 14px;
    padding: 12px;
    font-weight: 600;
    width: 100%;
    transition: 0.3s;
}

.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(255,140,0,0.25);
}

/* ---------- MOBILE ---------- */

@media (max-width: 768px) {

    .hero-title {
        font-size: 2.4rem;
    }

    .hero-subtitle {
        font-size: 1rem;
        padding: 0px 10px;
    }

    .stChatMessage {
        padding: 14px;
    }

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-thumb {
    background: #ff9500;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HERO ---------------- #

st.markdown("""
<div class="hero">
    <div class="hero-title">✈️ NextTrip Bot</div>
    <div class="hero-subtitle">
        Your Smart AI Travel Planner for Incredible India 🇮🇳
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ---------------- #

with st.sidebar:

    st.title("🌍 Features")

    st.markdown("""
    - 🕌 Tourist Places
    - 🍴 Food Recommendations
    - 💰 Budget Planner
    - 🗓️ Trip Itinerary
    - 🏔️ Hill Stations
    - 🏖️ Beaches
    - 🛕 Temple Tours
    - 🚕 Travel Guidance
    """)

    st.markdown("---")

    st.subheader("💡 Try Asking")

    st.info("3 day Goa trip under ₹10000")
    st.info("Best places in Kerala")
    st.info("2 day Ooty trip")
    st.info("Best food in Delhi")

# ---------------- QUICK BUTTONS ---------------- #

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🏖️ Goa"):
        st.session_state.example = "3 day Goa trip under ₹10000"

with col2:
    if st.button("🏔️ Hills"):
        st.session_state.example = "Best hill stations in India"

with col3:
    if st.button("🍴 Food"):
        st.session_state.example = "Best street foods in Delhi"

with col4:
    if st.button("🛕 Temples"):
        st.session_state.example = "South India temple trip"

# ---------------- CHAT HISTORY ---------------- #

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------- LLM ---------------- #

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.3,
)

# ---------------- SYSTEM PROMPT ---------------- #

SYSTEM_PROMPT = """
You are NextTrip Bot, an expert India travel planner AI.

Help users with:
- Trip itineraries
- Tourist attractions
- Food recommendations
- Budget planning
- Hotels
- Transport
- Beaches
- Hill stations
- Temples
- Adventure tourism

Always provide:
- Day-wise plans
- Budget estimation in INR
- Food suggestions
- Travel guidance
- Practical recommendations
"""

# ---------------- INPUT ---------------- #

default_prompt = st.session_state.get("example", "")

user_prompt = st.chat_input(
    "Ask about travel anywhere in India..."
)

if user_prompt or default_prompt:

    final_prompt = user_prompt if user_prompt else default_prompt

    st.chat_message("user").markdown(final_prompt)

    st.session_state.chat_history.append({
        "role": "user",
        "content": final_prompt
    })

    with st.spinner("Planning your trip ✨"):

        response = llm.invoke([
            {"role": "system", "content": SYSTEM_PROMPT},
            *st.session_state.chat_history
        ])

    assistant_response = response.content

    st.session_state.chat_history.append({
        "role": "assistant",
        "content": assistant_response
    })

    with st.chat_message("assistant"):
        st.markdown(assistant_response)
