from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq

# Load env
load_dotenv()

# Page setup
st.set_page_config(
    page_title="NextTrip Bot AI",
    page_icon="🇮🇳",
    layout="wide",
)

# ---------------- CSS ---------------- #
st.markdown("""
<style>

/* Background */
.stApp {
    background-color: #f8fafc;
    color: #111827;
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Main Title */
.main-title {
    font-size: 3.5rem;
    font-weight: 800;
    text-align: center;
    color: #ea580c;
    margin-top: 10px;
    font-family: 'Segoe UI', sans-serif;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #475569;
    font-size: 1.2rem;
    margin-bottom: 30px;
}

/* Chat Box */
.stChatMessage {
    background: white;
    border-radius: 18px;
    padding: 15px;
    margin-bottom: 15px;
    border: 1px solid #e2e8f0;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
    color: #111827;
    font-size: 16px;
    line-height: 1.7;
}

/* Input */
.stChatInput input {
    background-color: white !important;
    color: black !important;
    border-radius: 14px !important;
    border: 1px solid #cbd5e1 !important;
    padding: 12px !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: white;
    border-right: 1px solid #e5e7eb;
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    color: #111827 !important;
}

/* Buttons */
.stButton button {
    background: linear-gradient(90deg, #f97316, #ea580c);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 10px 18px;
    font-weight: 600;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-thumb {
    background: #f97316;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ---------------- #
st.markdown(
    '<div class="main-title">NextTrip Bot</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Your Smart India Travel Planner ✨</div>',
    unsafe_allow_html=True
)

# ---------------- SIDEBAR ---------------- #
with st.sidebar:

    st.title("🌍 Travel Features")

    st.markdown("""
    ### ✨ AI Features

    - 🕌 Tourist Attractions
    - 🍴 Food Recommendations
    - 💰 Budget Trip Planning
    - 🗓️ One-Day Itinerary
    - 🏔️ Hill Stations
    - 🏖️ Beaches
    - 🛕 Temple Tours
    - 🚕 Transport Guidance
    - 🏨 Hotel Suggestions
    - 👨‍👩‍👧 Family Trips
    - ❤️ Couple Trips
    - 🎒 Solo Travel Plans
    """)

    st.markdown("---")

    st.subheader("💡 Try Asking")

    st.info("3 day Goa trip under ₹10000")

    st.info("Best food places in Delhi")

    st.info("2 day Ooty family trip")

    st.info("Best places to visit in Kerala")

# ---------------- QUICK BUTTONS ---------------- #
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🏖️ Goa Trip"):
        st.session_state.example = "3 day Goa trip under ₹10000"

with col2:
    if st.button("🏔️ Hill Stations"):
        st.session_state.example = "Best hill stations in India"

with col3:
    if st.button("🍴 Food Tour"):
        st.session_state.example = "Best street foods in Delhi"

with col4:
    if st.button("🛕 Temple Tour"):
        st.session_state.example = "South India temple trip"

# ---------------- CHAT HISTORY ---------------- #
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display old messages
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
You are BharatYatra AI, an expert India travel planner.

You help users plan trips across India.

Your expertise includes:
- Tourist attractions
- Budget travel
- Luxury travel
- Food recommendations
- Family trips
- Couple trips
- Solo trips
- Beaches
- Hill stations
- Temples
- Adventure tourism
- Local transport
- Hotel recommendations

Always:
- Give detailed itineraries
- Mention estimated budgets in INR
- Suggest local foods
- Recommend transport options
- Mention best timings
- Keep responses visually attractive
- Use emojis moderately

If user asks:
"3 day Goa trip under ₹10000"

Generate:
- Day-wise itinerary
- Hotel suggestions
- Food recommendations
- Transport suggestions
- Budget breakdown
- Total estimated cost

Act like a professional India travel guide.
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

    with st.spinner("Planning your India trip ✨"):

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
