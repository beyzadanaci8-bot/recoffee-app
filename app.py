import streamlit as st
import pandas as pd
import time

# Page Layout Configuration
st.set_page_config(page_title="ReCoffee - Circular Economy Platform", page_icon="☕", layout="wide")

# Advanced Custom CSS for Premium UI/UX Experience
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    * { font-family: 'Poppins', sans-serif; }
    .stApp { background-color: #F9F6F0; }
    
    /* Premium Design Cards */
    .card {
        background: white;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.04);
        margin-bottom: 20px;
        border: 1px solid #EFEBE9;
    }
    .premium-card {
        background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%);
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(230,124,115,0.15);
        margin-bottom: 20px;
        border: 1px solid #FFB74D;
    }
    .green-accent-box {
        background-color: #E8F5E9;
        border-left: 5px solid #2E7D32;
        padding: 16px;
        border-radius: 8px;
        margin-bottom: 15px;
    }
    
    /* Typography */
    h1, h2, h3 { color: #3E2723 !important; font-weight: 600; }
    .brand-title { font-size: 3rem; font-weight: 700; color: #2E7D32 !important; margin-bottom: 0; }
    .brand-subtitle { font-size: 1.1rem; color: #795548; margin-top: 0; margin-bottom: 30px; }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);
        color: white;
        border-radius: 25px;
        border: none;
        padding: 12px 30px;
        font-weight: 600;
        box-shadow: 0 4px 10px rgba(46, 125, 50, 0.2);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(46, 125, 50, 0.3);
        color: white;
    }
    
    /* Chat Bubble */
    .chat-bubble-user { background-color: #EFEBE9; padding: 12px 16px; border-radius: 12px 12px 0 12px; margin-bottom: 10px; text-align: right; color: #3E2723; }
    .chat-bubble-bot { background-color: #E8F5E9; padding: 12px 16px; border-radius: 12px 12px 12px 0; margin-bottom: 20px; border-left: 4px solid #2E7D32; color: #1B5E20; }
    </style>
""", unsafe_allow_html=True)

# State Management Optimization
if 'cafe_waste_balance' not in st.session_state: st.session_state.cafe_waste_balance = 35.0
if 'producer_collected_waste' not in st.session_state: st.session_state.producer_collected_waste = 48.0  # Simulated collection for producers
if 'is_premium' not in st.session_state: st.session_state.is_premium = False
if 'is_auth' not in st.session_state: st.session_state.is_auth = False
if 'cart' not in st.session_state: st.session_state.cart = []
if 'expert_chat_history' not in st.session_state: st.session_state.expert_chat_history = []

# --- EXTENDED MARKET CATALOG ---
market_catalog = {
    "Premium Bio-Espresso Cup": {"origin": "Brew Mood Alsancak", "price": 145, "desc": "100% upcycled structure, heat-resistant casing."},
    "Nitrogen-Rich Soil Nutrient (2kg)": {"origin": "Two Cup Bornova", "price": 80, "desc": "Perfected additive formulation for acidic crops."},
    "Exfoliating Coffee Body Scrub": {"origin": "Coffee Güzelyalı", "price": 110, "desc": "Organic cosmetic material sourced directly from local artisans."},
    "Eco Bio-Fuel Pellets (Bulk)": {"origin": "İzmir Bio-Factory", "price": 220, "desc": "Compressed alternate bio-energy resource for industrial systems."}
}

# --- AUTHENTICATION SCREEN ---
if not st.session_state.is_auth:
    col_l, col_c, col_r = st.columns([1, 1.5, 1])
    with col_c:
        st.markdown("<div class='card' style='margin-top: 50px; text-align: center;'>", unsafe_allow_html=True)
        st.markdown("<h1 class='brand-title'>ReCoffee</h1>", unsafe_allow_html=True)
        st.markdown("<p class='brand-subtitle'>\"Your morning coffee, changed.\"</p>", unsafe_allow_html=True)
        
        email_inp = st.text_input("Corporate / Individual Email", placeholder="example@cafe.com")
        pass_inp = st.text_input("Security Key", type="password", placeholder="••••••••")
        user_role_inp = st.selectbox("Ecosystem Role", [
            "Independent Local Cafe (Segment A)", 
            "Large Coffee Chain (Segment B)", 
            "Local Composter / Urban Farmer (Segment C)", 
            "Sustainable Manufacturer (Segment D)"
        ])
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Access Circular Bridge", use_container_width=True):
            st.session_state.is_auth = True
            st.session_state.role_string = user_role_inp
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# --- MAIN DASHBOARD HUB ---
else:
    # Sidebar Layout
    st.sidebar.markdown("<h2 style='text-align: center; color: #2E7D32 !important;'>ReCoffee Portal</h2>", unsafe_allow_html=True)
    st.sidebar.markdown(f"<p style='text-align: center; color: #795548; font-size: 0.85rem;'>Active Role:<br><b>{st.session_state.role_string}</b></p>", unsafe_allow_html=True)
    
    # Premium / Subscription Status Badge in Sidebar
    if st.session_state.is_premium:
        st.sidebar.markdown("<div style='text-align:center; background-color:#E8F5E9; color:#2E7D32; padding:5px; border-radius:10px; font-weight:bold; border:1px solid #2E7D32;'>👑 BRIDGE PREMIUM ACTIVE</div>", unsafe_allow_html=True)
    else:
        st.sidebar.markdown("<div style='text-align:center; background-color:#FFE0B2; color:#E65100; padding:5px; border-radius:10px; font-weight:bold; border:1px solid #FFB74D;'>⚙️ TRIAL ACCOUNT (Max 50kg)</div>", unsafe_allow_html=True)
        
    st.sidebar.markdown("---")
    
    nav_selection = st.sidebar.radio("Navigation Hub", [
        "🗺️ The Bridge (Live GPS & Maps)", 
        "🏪 Cafe Portal & Milestones",
        "💎 B2B Subscription & Quota Hub",
        "🔬 Expert Guidance & Live Q&A", 
        "🛒 Eco-Marketplace & Checkout"
    ])
    
    st.sidebar.markdown("---")
    if st.sidebar.button("Secure Logout", use_container_width=True):
        st.session_state.is_auth = False
        st.rerun()

    # SECTION 1: THE BRIDGE (LIVE MAPS & EMISSION METRICS)
    if nav_selection == "🗺️ The Bridge (Live GPS & Maps)":
        st.markdown("<h1>The Bridge: Live Waste Tracker</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #795548;'>Advanced B2B matching ecosystem pairing regional organic waste with verified local producers.</p>", unsafe_allow_html=True)
        
        # Checking Subscription Block for Map Content
        if not st.session_state.is_premium and st.session_state.producer_collected_waste >= 50.0:
            st.error("🔒 **Bridge Map Locked!** You have reached your **50 kg free trial allocation limit**. To unlock live GPS matching, automated logistics tracking, and source unlimited grounds, please subscribe to **Bridge Premium** in the Quota Hub.")
        else:
            m1, m2, m3 = st.columns(3)
            total_kg = st.session_state.cafe_waste_balance + 20.0 + 32.0
            m1.metric("Total Available Grounds (İzmir Area)", f"{total_kg:.1f} kg")
            m2.metric("Target UN SDG Framework Alignment", "SDG 12 & 13")
            m3.metric("Active Environmental Hubs", "3 Hotspots Connected")
            
            st.markdown("### 📍 Live Spatial GPS Mapping (İzmir)")
            map_df = pd.DataFrame({
                'lat': [38.4385, 38.4633, 38.3244],
                'lon': [27.1432, 27.2167, 26.7644],
                'name': ['Brew Mood Alsancak (15kg)', 'Two Cup Bornova (20kg)', 'Port Coffee Urla (32kg)']
            })
            st.map(map_df, size=15)
            
            st.markdown("### 📊 Nearby Hub Optimization Analytics")
            hotspots_df = pd.DataFrame({
                "Hotspot Location": ["Brew Mood Alsancak", "Two Cup Bornova", "Port Coffee Urla"],
                "Proximity Radius": ["1.2 km", "4.5 km", "12.5 km"],
                "Verified Quantity": [f"{st.session_state.cafe_waste_balance} kg", "20.0 kg", "32.0 kg"],
                "Quality Compliance": ["Premium (Moisture <5%)", "Standard Level", "Pending Lab Verification"]
            })
            st.dataframe(hotspots_df, use_container_width=True)

    # SECTION 2: CAFE PORTAL & GREEN BADGE TRACKER
    elif nav_selection == "🏪 Cafe Portal & Milestones":
        st.markdown("<h1>Cafe Corporate Portal</h1>", unsafe_allow_html=True)
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### 🛡️ 50 kg Trial Rule Quota Tracking (For Cafes)")
        current_vol = st.session_state.cafe_waste_balance
        st.progress(min(current_vol / 50.0, 1.0))
        
        if current_vol >= 50.0:
            st.success("🎉 **Ecosystem Milestone Reached:** You unlocked the ReCoffee **'Green Badge'** and your physical window sticker QR code!")
        else:
            st.warning(f"💡 Log exactly **{50.0 - current_vol:.1f} kg** more to secure your verified Green Badge status.")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### 📈 Log Waste Dispatch")
        new_metric = st.number_input("Input Coffee Grounds Weight to Dispatch (kg):", min_value=0.0, step=1.0)
        if st.button("Confirm & Log Grounds", use_container_width=True):
            st.session_state.cafe_waste_balance += new_metric
            st.success(f"Metrics Updated! Linked {new_metric} kg into the active life cycle.")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # 🔥 NEW SECTION 3: B2B SUBSCRIPTION & 60 KG QUOTA HUB
    elif nav_selection == "💎 B2B Subscription & Quota Hub":
        st.markdown("<h1>B2B Subscription & Quota Management</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #795548;'>Value-Based Segmented Pricing Core. Control your raw material allowance tier parameters.</p>", unsafe_allow_html=True)
        
        col_sub1, col_sub2 = st.columns([1.5, 1])
        
        with col_sub1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("### 📊 Your Active Collection Volume Analytics")
            collected = st.session_state.producer_collected_waste
            st.write(f"You have currently sourced **{collected:.1f} kg** of organic waste grounds from local cafes via The Bridge.")
            
            # Quota Visualization Bar
            if not st.session_state.is_premium:
                st.write("🔴 **Trial Capacity Limit Indicator (Max 50 kg):**")
                st.progress(min(collected / 50.0, 1.0))
                if collected >= 50.0:
                    st.error("⚠️ **Quota Blockade:** You have hit the **50 kg free allocation limit**. Sourcing any more coffee waste grounds requires a premium account tier activation.")
                else:
                    st.info(f"💡 You have **{50.0 - collected:.1f} kg** left before your account automatically switches to restricted viewing mode.")
            else:
                st.write("🟢 **Bridge Premium Plan Active (Unlimited Quota Structure):**")
                st.progress(1.0)
                st.success("✨ Sourcing is completely **unlimited**! You have active bypass authority over the 50 kg restriction barrier, allowing large-scale industrial manufacturing extraction loops.")
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Interactive Simulation Action
            if not st.session_state.is_premium and collected < 50.0:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown("### 🚜 Simulate Sourcing More Material (Test the Barrier)")
                sim_add = st.number_input("Enter amount to collect from nearby cafes (kg):", min_value=0.0, step=5.0, value=5.0)
                if st.button("Collect via The Bridge"):
                    st.session_state.producer_collected_waste += sim_add
                    st.toast(f"Successfully sourced {sim_add} kg of grounds!")
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

        with col_sub2:
            st.markdown("<div class='premium-card' style='text-align: center;'>", unsafe_allow_html=True)
            st.markdown("<h3>👑 Bridge Premium Tier</h3>", unsafe_allow_html=True)
            st.markdown("<h2 style='color:#E65100 !important;'>450 TL <span style='font-size:1rem; color:#795548;'>/ month</span></h2>", unsafe_allow_html=True)
            st.markdown("""
                <p style='font-size:0.85rem; text-align:left; color:#5D4037;'>
                🔓 <b>Unlock full map functionality & real-time GPS</b><br>
                🚀 <b>Bypass the 50 kg Trial Rule blockade</b><br>
                📈 <b>Unlimited large-scale raw material supply logs</b><br>
                🏢 <b>Tailored pricing models for B2B Manufacturers</b>
                </p>
            """, unsafe_allow_html=True)
            
            if st.session_state.is_premium:
                if st.button("Cancel Subscription", key="cancel_sub", use_container_width=True):
                    st.session_state.is_premium = False
                    st.session_state.producer_collected_waste = 40.0  # Reset below barrier for safety testing
                    st.success("Subscription downgraded to standard trial mode.")
                    st.rerun()
            else:
                if st.button("Activate Bridge Premium", key="activate_sub", use_container_width=True):
                    st.session_state.is_premium = True
                    st.success("🎉 Welcome to Bridge Premium! Your unlimited extraction bypass parameters are now officially authorized.")
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    # SECTION 4: EXPERT GUIDANCE & LIVE Q&A CHAT CONSOLE
    elif nav_selection == "🔬 Expert Guidance & Live Q&A":
        st.markdown("<h1>Expert Consultation Portal</h1>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("### 🧪 Soil Chemistry Matrix")
            st.markdown("<div class='green-accent-box'><b>Average Parameter Range: 5.8 - 6.2 pH</b></div>", unsafe_allow_html=True)
            st.write("Mildly acidic profile. Highly optimal for local citrus vegetation and roses across the Aegean region.")
            st.markdown("</div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("### 🪱 Integrity Guidance Protocols")
            st.write("• **Mold Prevention:** Dry extraction logs within **24 hours**.")
            st.write("• **Industrial Bio-Fuel:** Moisture thresholds must remain **below 5%**.")
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("### 💬 Live Interactive Agronomy Portal")
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        for chat in st.session_state.expert_chat_history:
            if chat['role'] == 'user': st.markdown(f"<div class='chat-bubble-user'><b>You:</b> {chat['text']}</div>", unsafe_allow_html=True)
            else: st.markdown(f"<div class='chat-bubble-bot'><b>Agronomist AI:</b> {chat['text']}</div>", unsafe_allow_html=True)
        
        user_query = st.text_input("Ask a question about crop alignment, mushroom substrate setups, or moisture management:")
        if st.button("Submit Question to Expert Panel"):
            if user_query:
                st.session_state.expert_chat_history.append({'role': 'user', 'text': user_query})
                response_text = "Coffee grounds maintain a premium nitrogen-dense profile. Since their parameters average 5.8-6.2 pH, they are perfect for citrus crops. Ensure they are dried within 24 hours to mitigate mold risks!"
                if "mushroom" in user_query.lower(): response_text = "Oyster mushrooms thrive on coffee substrates due to high base nitrogen availability. Ensure moisture controls stay balanced."
                st.session_state.expert_chat_history.append({'role': 'bot', 'text': response_text})
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # SECTION 5: ECO-MARKETPLACE & CHECKOUT PAYMENT MODULE
    elif nav_selection == "🛒 Eco-Marketplace & Checkout":
        st.markdown("<h1>The Eco-Marketplace & Checkout Terminal</h1>", unsafe_allow_html=True)
        col_m1, col_m2 = st.columns([2, 1])
        
        with col_m1:
            st.markdown("### 🛍️ Available Upcycled Products Catalog")
            for title, info in market_catalog.items():
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                cols = st.columns([3, 1])
                with cols[0]:
                    st.markdown(f"#### {title}")
                    st.markdown(f"<p style='color: #2E7D32; font-size: 0.85rem; margin: 0;'><b>Sourced From:</b> {info['origin']}</p>", unsafe_allow_html=True)
                    st.write(info['desc'])
                with cols[1]:
                    st.markdown(f"<h3 style='text-align: center; margin-top:10px;'>{info['price']} TL</h3>", unsafe_allow_html=True)
                    if st.button("Add to Batch", key=title):
                        st.session_state.cart.append({"title": title, "price": info['price']})
                        st.toast(f"{title} appended to configuration order!")
                        st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
                
        with col_m2:
            st.markdown("### 🛒 Your Order Review")
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            if not st.session_state.cart:
                st.write("*Your shopping cart is currently empty.*")
                total_price = 0
            else:
                total_price = 0
                for item in st.session_state.cart:
                    st.write(f"• {item['title']} — {item['price']} TL")
                    total_price += item['price']
                st.markdown("---")
                st.markdown(f"#### **Total Due: {total_price} TL**")
                if st.button("Clear Order Batch", use_container_width=True):
                    st.session_state.cart = []
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
            
            if total_price > 0:
                st.markdown("### 💳 Secure Payment Checkout")
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                card_name = st.text_input("Cardholder Full Name", placeholder="John Doe")
                card_num = st.text_input("Card Account Number", placeholder="0000 0000 0000 0000", max_chars=19)
                col_exp1, col_exp2 = st.columns(2)
                col_exp1.text_input("Expiry Date", placeholder="MM/YY", max_chars=5)
                col_exp2.text_input("CVC Security Code", type="password", placeholder="***", max_chars=3)
                
                if st.button("Authorize Order Payment", use_container_width=True):
                    if card_name and card_num:
                        with st.spinner("Processing transaction secure payment..."): time.sleep(2)
                        st.success(f"🎉 Payment of {total_price} TL Authorized! Thank you for closing the loop with ReCoffee!")
                        st.session_state.cart = []
                    else: st.error("Please fill out the payment details.")
                st.markdown("</div>", unsafe_allow_html=True)
