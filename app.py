import streamlit as st
import pandas as pd

# 1. Page Configuration (Uygulamanın Tarayıcı Başlığı)
st.set_page_config(page_title="ReCoffee - Your Waste Bridge", page_icon="☕", layout="centered")

# 2. ReCoffee Renkleri ve Tasarımı (Projenizdeki Doğal Yeşil ve Kahve Tonları)
st.markdown("""
    <style>
    .stApp { background-color: #FDFBF7; }
    h1, h2, h3 { color: #3E2723 !important; font-family: 'Helvetica Neue', sans-serif; }
    .stButton>button { background-color: #4CAF50; color: white; border-radius: 20px; border: none; padding: 10px 24px; font-weight: bold; }
    .stButton>button:hover { background-color: #388E3C; color: white; }
    .badge-box { padding: 20px; background-color: #E8F5E9; border-radius: 10px; border-left: 5px solid #2E7D32; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# 3. Uygulama Hafızasını Başlatma (İlk veriler)
if 'cafe_waste' not in st.session_state: st.session_state.cafe_waste = 35.0
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

# --- EKRAN 1: GİRİŞ EKRANI (AUTHENTICATION) ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>ReCoffee</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #795548;'>Your bridge to zero waste</p>", unsafe_allow_html=True)
    
    email = st.text_input("Enter Email")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["Individual (Shopper)", "Independent Cafe", "Large Coffee Chain", "Sustainable Manufacturer"])
    
    if st.button("Sign In"):
        st.session_state.logged_in = True
        st.session_state.user_role = role
        st.rerun()

# --- ANA UYGULAMA EKRANLARI ---
else:
    # Sol Menü (Navigasyon)
    st.sidebar.title("ReCoffee Navigation")
    app_mode = st.sidebar.radio("Go to", ["The Bridge (Live Tracker)", "Cafe Portal", "Expert Guidance", "Eco-Market"])
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # EKRAN A: THE BRIDGE (Canlı Atık Takibi)
    if app_mode == "The Bridge (Live Tracker)":
        st.title("The Bridge: Live Waste Tracker")
        st.markdown("Real-time GPS coffee ground stations in İzmir.")
        
        total_available = st.session_state.cafe_waste + 20.0 + 12.0
        st.metric(label="Total Active Waste Available (İzmir Area)", value=f"{total_available} kg")
        
        hotspots_data = {
            "Cafe Name": ["Brew Mood Alsancak", "Two Cup Bornova", "Coffeeshop Urla"],
            "Distance": ["1.2 km", "4.5 km", "12.5 km"],
            "Available Grounds": [f"{st.session_state.cafe_waste} kg", "20.0 kg", "12.0 kg"],
            "Quality Standard": ["Verified (Moisture <5%)", "Verified", "Pending"]
        }
        st.dataframe(pd.DataFrame(hotspots_data), use_container_width=True)
        st.info("💡 GPS matching minimizes transportation emissions, actively supporting UN SDG 13 (Climate Action).")

    # EKRAN B: CAFE PORTAL (Atık Girişi ve Rozet Durumu)
    elif app_mode == "Cafe Portal":
        st.title("Cafe Portal")
        st.subheader(f"Welcome back, Partner! ({st.session_state.user_role})")
        current_waste = st.session_state.cafe_waste
        
        st.markdown("<div class='badge-box'>", unsafe_allow_html=True)
        st.markdown(f"### 🛡️ Green Badge Progress: {current_waste:.1f} / 50.0 kg")
        st.progress(min(current_waste / 50.0, 1.0))
        
        if current_waste >= 50.0: 
            st.success("🎉 Congratulations! You unlocked the ReCoffee 'Green Badge'!")
        else: 
            st.warning(f"💡 Log {50.0 - current_waste:.1f} kg more to become a certified Green Partner!")
        st.markdown("</div>", unsafe_allow_html=True)
        
        new_log = st.number_input("Enter coffee grounds weight to log (kg):", min_value=0.0, step=0.5)
        if st.button("Log Grounds"):
            st.session_state.cafe_waste += new_log
            st.success(f"Successfully logged {new_log} kg!")
            st.rerun()

    # EKRAN C: EXPERT GUIDANCE (Tarım ve pH Bilgileri)
    elif app_mode == "Expert Guidance":
        st.title("Expert Guidance")
        st.markdown("Agricultural & biological insights for organic waste utilization.")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🧪 pH Balance Check")
            st.write("Spent coffee grounds have an average pH of **5.8 - 6.2** (Acidic).")
            st.write("Great for: Citrus plants and roses in İzmir's soil profile.")
        with col2:
            st.subheader("🪱 Recycling Tips")
            st.write("Dry the grounds within **24 hours** to prevent mold growth.")

    # EKRAN D: ECO-MARKET (İleri Dönüşüm Ürünleri)
    elif app_mode == "Eco-Market":
        st.title("Eco-Market")
        st.markdown("Shop unique products derived directly from upcycled coffee grounds.")
        products = [
            {"name": "Bio-Espresso Cup", "source": "Brew Mood Alsancak", "price": "145 TL"},
            {"name": "Soil Nutrient (2kg)", "source": "Two Cup Bornova", "price": "80 TL"},
            {"name": "Coffee Body Scrub", "source": "Coffee Güzelyalı", "price": "110 TL"}
        ]
        for p in products:
            st.markdown(f"### {p['name']} - {p['price']}")
            st.markdown(f"*From: {p['source']}*")
            st.markdown("---")
