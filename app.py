"""
Government Scheme Navigator — Streamlit Chat UI
Discover schemes you're eligible for. Apply with confidence.
"""
import streamlit as st
import os
from agent.core import SchemeAgent

st.set_page_config(
    page_title="🏛️ Yojana Saathi — Scheme Navigator",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #ff6f00, #ff9800);
        color: white; padding: 1.5rem 2rem; border-radius: 12px;
        margin-bottom: 1rem; text-align: center;
    }
    .scheme-card {
        background: #fff3e0; border-left: 4px solid #ff6f00;
        padding: 1rem; border-radius: 8px; margin-bottom: 0.75rem;
    }
    .benefit-badge {
        background: #4caf50; color: white; border-radius: 20px;
        padding: 4px 12px; font-size: 0.85rem; font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


def init_session():
    if "agent" not in st.session_state:
        st.session_state.agent = None
    if "messages" not in st.session_state:
        st.session_state.messages = []


def sidebar():
    with st.sidebar:
        st.title("🏛️ Yojana Saathi")
        st.caption("Government Scheme Navigator")

        st.divider()

        api_key = st.text_input("🔑 Groq API Key", type="password", placeholder="gsk_...", help="Free at console.groq.com")
        if api_key and not st.session_state.agent:
            st.session_state.agent = SchemeAgent(api_key=api_key, provider="groq")
            st.success("✅ Ready!")

        st.divider()

        # Eligibility quick check
        st.subheader("📋 Quick Eligibility Check")
        age = st.number_input("Your Age", 0, 100, 25)
        gender = st.selectbox("Gender", ["male", "female", "other"])
        occupation = st.selectbox("Occupation", ["farmer", "student", "worker", "business", "unemployed", "retired", "other"])
        income = st.selectbox("Annual Family Income", ["below_1lakh", "1_3lakh", "3_5lakh", "above_5lakh"])
        category = st.selectbox("Category", ["general", "sc", "st", "obc"])

        if st.button("🔍 Find My Schemes", use_container_width=True):
            query = f"I am {age} years old, {gender}, work as {occupation}, family income is {income.replace('_', ' ')}, category is {category}. What schemes am I eligible for?"
            st.session_state.pending_message = query
            st.rerun()

        st.divider()

        st.subheader("⚡ Quick Questions")
        for q in [
            "Kisan Credit Card kaise banwayen?",
            "Free hospital treatment ke liye kya karein?",
            "Mujhe loan chahiye business ke liye",
            "Scholarship kaise milegi?",
            "Old age pension ke liye apply kaise karein?",
        ]:
            if st.button(q, use_container_width=True, key=f"q_{q[:20]}"):
                st.session_state.pending_message = q
                st.rerun()

        st.divider()
        st.caption("By [Nawang Dorjay](https://github.com/nawangdorjay) — GSSoC 2026")


def main():
    init_session()
    sidebar()

    st.markdown("""
    <div class="main-header">
        <h1>🏛️ Yojana Saathi</h1>
        <p style="font-size:1.1rem; margin:0;">Find government schemes you're eligible for — agriculture, health, education, housing, business</p>
        <p style="font-size:0.9rem; margin:0.5rem 0 0 0; opacity:0.9;">18 schemes • Eligibility matching • Documents checklist • Step-by-step application guide</p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.messages:
        cols = st.columns(3)
        for i, (title, desc, amount) in enumerate([
            ("🌾 PM-KISAN", "Direct income for farmers", "₹6,000/year"),
            ("🏥 Ayushman Bharat", "Free hospital treatment", "₹5 lakh/year"),
            ("🏠 PM Awas", "Pucca house subsidy", "₹1.2-2.67L"),
            ("💼 MUDRA Loan", "Business loan without collateral", "Up to ₹10L"),
            ("📚 Scholarship", "Education support for SC/ST/OBC", "₹230-1200/mo"),
            ("👩 Ujjwala Yojana", "Free LPG for women", "Free connection"),
        ]):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="scheme-card">
                    <b>{title}</b><br>
                    <span style="font-size:0.9rem;">{desc}</span><br>
                    <span class="benefit-badge">{amount}</span>
                </div>
                """, unsafe_allow_html=True)

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.session_state.pop("pending_message", None) or st.chat_input("कौन सी योजना चाहिए? Which scheme do you need?")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        if not st.session_state.agent:
            msg = "⚠️ Please enter your Groq API key in the sidebar."
            st.session_state.messages.append({"role": "assistant", "content": msg})
            with st.chat_message("assistant"):
                st.warning(msg)
            return

        with st.chat_message("assistant"):
            with st.spinner("🔍 Finding schemes..."):
                response = st.session_state.agent.process_query(prompt)
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

    st.divider()
    st.caption("Data sourced from official government portals. Verify at respective websites.")


if __name__ == "__main__":
    main()
