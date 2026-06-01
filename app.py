import streamlit as st
import pandas as pd
import time

# Page Layout & Style Configuration
st.set_page_config(page_title="ReCoffee - Circular Economy Platform", page_icon="☕", layout="wide")

# Advanced Custom CSS for Premium UI/UX Experience
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    * { font-family: 'Poppins', sans-serif; }
    .stApp { background-color: #F9F6F0; }
    
    /* Premium B2B Cards */
    .card {
        background: white;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.04);
        margin-bottom: 20px;
        border: 1px solid #EFEBE9;
    }
    
    .green-accent-box {
        background-color: #E8F5E9;
        border-left: 5px solid #2E7D32;
        padding: 16px;
        border-radius: 8px;
        margin-bottom: 15px;
    }
    
    /* Headers & Typography */
    h1, h2, h3 { color: #3E2723 !important; font-weight: 600; }
    .brand-title { font-size: 3rem; font-weight: 700; color: #2E7D32 !important; margin-bottom: 0; }
    .brand-subtitle { font-size: 1.1rem; color: #795548; margin-top: 0; margin-bottom: 30px; }
    
    /* Modern Linear Gradient Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);
        color: white;
        border-radius: 25px;
        border: none;
        padding: 12px 30px;
        font-weight: 600;
        box-shadow: 0 4px 10px rgba(46, 125, 50, 0.2);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(46, 125, 50, 0.3);
        color: white;
    }
    
    /* Chat & Q&A Styling */
    .chat-bubble-user {
        background-color: #EFEBE9;
        padding: 12px 16px;
        border-radius: 12px 12px 0 12px;
        margin-bottom: 10px;
        text-align: right;
        color: #3E2723;
    }
    .chat-bubble-bot {
        background-color: #E8F5E9;
        padding: 12px 16px;
        border-radius: 12px 12px 12px 0;
        margin-bottom: 20px;
        border-left: 4px solid #2E7D32;
        color: #1B5E20;
    }
    </style>
""", unsafe_allow_html=True)

# Advanced State Management for Interactive Logic
if 'cafe_waste_balance' not in st.session_state: st.session_state.cafe_waste_balance = 35.0
if 'is_auth' not in st.session_state: st.session_state.is_auth = False
if 'cart' not in st.session_state: st.session_state.cart = []
if 'expert_chat_history' not in st.session_state: st.session_state.expert_chat_history = []

# --- EXTENDED MARKET DICTIONARY ---
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
    st.sidebar.markdown("---")
    
    nav_selection = st.sidebar.radio("Navigation Hub", [
        "🗺️ The Bridge (Live GPS & Info)", 
        "🏪 Cafe Portal & Milestones", 
        "🔬 Expert Guidance & Live Q&A", 
        "🛒 Eco-Marketplace & Checkout"
    ])
    
    st.sidebar.markdown("---")
    if st.sidebar.button("Secure Logout", use_container_width=True):
        st.session_state.is_auth = False
        st.rerun()

    # SECTION 1: THE BRIDGE (LIVE GPS MAP & GENERAL INFO MATRIX)
    if nav_selection == "🗺️ The Bridge (Live GPS & Info)":
        st.markdown("<h1>The Bridge: Live Waste Tracker</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #795548;'>Advanced B2B matching ecosystem pairing regional organic waste with verified local producers.</p>", unsafe_allow_html=True)
        
        # Upper Core Metrics
        m1, m2, m3 = st.columns(3)
        total_kg = st.session_state.cafe_waste_balance + 20.0 + 32.0
        m1.metric("Total Available Grounds (İzmir Area)", f"{total_kg:.1f} kg")
        m2.metric("Target UN SDG Framework Alignment", "SDG 12 & 13")
        m3.metric("Active Environmental Hubs", "3 Hotspots Connected")
        
        st.markdown("### 📍 Live Spatial GPS Mapping (İzmir)")
        map_df = pd.DataFrame({
            'lat': [38.4385, 38.4633, 38.3244],
            'lon': [27.1432, 27.2167, 26.7644],
            'name': ['Brew Mood Alsancak (15kg ready)', 'Two Cup Bornova (20kg ready)', 'Port Coffee Urla (32kg ready)']
        })
        st.map(map_df, size=15)
        
        # General Information / How It Works Matrix
        st.markdown("### ℹ️ Core Ecosystem Mechanics & Value Proposition")
        col_inf1, col_inf2 = st.columns(2)
        with col_inf1:
            st.markdown("""
            <div class='card'>
                <h4>🌱 Supporting SDG 12: Responsible Consumption</h4>
                <p style='font-size: 0.9rem; color: #5d4037;'>
                Coffee grounds are nutrient-dense resources containing essential micronutrients like nitrogen, phosphorus, and magnesium. 
                Instead of allowing them to degrade in local landfills, ReCoffee upcycles them directly into bio-fertilisers and mushroom substrates.
                </p>
            </div>
            """, unsafe_allow_html=True)
        with col_inf2:
            st.markdown("""
            <div class='card'>
                <h4>🌍 Supporting SDG 13: Climate Action</h4>
                <p style='font-size: 0.9rem; color: #5d4037;'>
                Decomposing coffee grounds release high levels of methane, a potent greenhouse gas accelerating global warming. 
                By utilizing real-time GPS tracking and smart scheduling, we pair local collectors instantly to minimize transportation carbon footprints.
                </p>
            </div>
            """, unsafe_allow_html=True)

    # SECTION 2: CAFE PORTAL & GREEN BADGE TRACKER
    elif nav_selection == "🏪 Cafe Portal & Milestones":
        st.markdown("<h1>Cafe Corporate Portal</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #795548;'>Track your environmental milestones, log volume metrics, and unlock green badges.</p>", unsafe_allow_html=True)
        
        col_p1, col_p2 = st.columns([1.5, 1])
        with col_p1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("### 🛡️ 50 kg Trial Rule Quota Tracking")
            current_vol = st.session_state.cafe_waste_balance
            prog = min(current_vol / 50.0, 1.0)
            st.progress(prog)
            
            if current_vol >= 50.0:
                st.success("🎉 **Ecosystem Milestone Reached:** Your establishment has officially unlocked the ReCoffee **'Green Badge'** and a physical window sticker with a digital impact tracking QR code!")
            else:
                st.warning(f"🔒 **Status: Standard Partner.** Log exactly **{50.0 - current_vol:.1f} kg** more to secure your verified Green Badge status.")
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("### 📈 Log Waste Dispatch")
            new_metric = st.number_input("Input Coffee Grounds Weight to Dispatch (kg):", min_value=0.0, step=1.0)
            if st.button("Confirm & Log Grounds", use_container_width=True):
                st.session_state.cafe_waste_balance += new_metric
                st.success(f"Metrics Updated! Linked {new_metric} kg into the active circular lifecycle framework.")
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_p2:
            st.markdown("<div class='card' style='text-align:center;'>", unsafe_allow_html=True)
            st.markdown("### 🛡️ Active Certification Status")
            if st.session_state.cafe_waste_balance >= 50.0:
                st.markdown("<p style='font-size:5rem; margin:0;'>🟢</p>", unsafe_allow_html=True)
                st.markdown("**GREEN PARTNER AUTHORIZED**<br>*Eco-friendly brand image active.*", unsafe_allow_html=True)
            else:
                st.markdown("<p style='font-size:5rem; margin:0;'>🟡</p>", unsafe_allow_html=True)
                st.markdown("**TRIAL PHASE ACTIVE**<br>*Complete 50kg quota to scale your tier.*", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # SECTION 3: EXPERT AGRICULTURAL GUIDANCE & INTERACTIVE INDIVIDUAL Q&A
    elif nav_selection == "🔬 Expert Guidance & Live Q&A":
        st.markdown("<h1>Expert Consultation & Live Interactive Q&A</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #795548;'>B2B expert consulting portal for strategic urban crop planning and personalized bio-material analytics.</p>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("### 🧪 Soil Chemistry & pH Matrix")
            st.markdown("<div class='green-accent-box'><b>Average Sample Parameter Range: 5.8 - 6.2 pH</b></div>", unsafe_allow_html=True)
            st.write("Due to nitrogen-dense and mildly acidic compounds, spent grounds are highly optimal for local acidic soil variations in the Aegean region.")
            st.write("🌿 **Highly Compatible Biota:** Citrus variations, blueberries, and local roses.")
            st.markdown("</div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("### 🪱 Supply Chain Integrity Guidance")
            st.write("1. **Mold Prevention Protocol:** All cafes must dry or isolate damp grounds within **24 hours** from extraction.")
            st.write("2. **Industrial Bio-Fuel Matrix:** Moisture threshold constants must stay **below 5%** to process raw outputs cleanly into pellets.")
            st.markdown("</div>", unsafe_allow_html=True)

        # INTERACTIVE INDIVIDUAL Q&A CHAT CONSOLE
        st.markdown("### 💬 Ask a Personal Sustainability/Agronomy Consultant")
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        
        # Display Chat History
        for chat in st.session_state.expert_chat_history:
            if chat['role'] == 'user':
                st.markdown(f"<div class='chat-bubble-user'><b>You:</b> {chat['text']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='chat-bubble-bot'><b>Agronomist AI:</b> {chat['text']}</div>", unsafe_allow_html=True)
                
        # Question Input Area
        user_query = st.text_input("Type your specific question about soil match, recycling, or bio-materials:", key="chat_input_box", placeholder="e.g., Can I use coffee grounds for growing mushrooms or citrus plants in Bornova soil?")
        
        if st.button("Submit Question to Expert Portal"):
            if user_query:
                # Add User Query to History
                st.session_state.expert_chat_history.append({'role': 'user', 'text': user_query})
                
                # Rule-Based Intelligent Bot Response Generation Simulation
                response_text = "Thank you for reaching out to the ReCoffee consulting team. Spent coffee grounds are rich in nitrogen, phosphorus, and magnesium, making them a premium organic additive. Since they maintain an acidic pH profile (5.8 - 6.2), your request is highly compatible for crop variations like citrus fruits or roses. Ensure you dry the grounds within 24 hours to prevent mold before application!"
                if "mushroom" in user_query.lower():
                    response_text = "Excellent inquiry! Spent coffee grounds make a fantastic sterile substrate for mushroom cultivation (especially oyster mushrooms) because they are rich in essential nitrogen and micronutrients. Make sure to keep the moisture profile well-regulated during incubation."
                elif "moisture" in user_query.lower() or "fuel" in user_query.lower():
                    response_text = "For industrial applications like bio-fuel pellets, maintaining a moisture matrix strictly below 5% is vital to achieve ideal compression ratios. Always enforce the 24-hour drying protocol at your source cafes."
                
                st.session_state.expert_chat_history.append({'role': 'bot', 'text': response_text})
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # SECTION 4: INTERACTIVE ECO-MARKETPLACE & SIMULATED CHECKOUT MODULE
    elif nav_selection == "🛒 Eco-Marketplace & Checkout":
        st.markdown("<h1>The Eco-Marketplace & Checkout Terminal</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #795548;'>Value-based pricing architecture model centered around local circularity and estimated carbon offsets.</p>", unsafe_allow_html=True)
        
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
                for index, item in enumerate(st.session_state.cart):
                    col_c1, col_c2 = st.columns([3, 1])
                    col_c1.write(f"• {item['title']}")
                    col_c2.write(f"{item['price']} TL")
                    total_price += item['price']
                
                st.markdown("---")
                st.markdown(f"#### **Total Due: {total_price} TL**")
                
                if st.button("Clear Order Batch", use_container_width=True):
                    st.session_state.cart = []
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Simulated Checkout Payment Terminal Panel
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
                        with st.spinner("Processing transaction via secure local bridge banking network..."):
                            time.sleep(2)  # Simulated server processing lag
                        st.success(f"🎉 Payment of {total_price} TL Authorized! Order sent to local logistics dispatcher. Thank you for closing the loop with ReCoffee!")
                        st.session_state.cart = []  # Clear cart on successful purchase simulation
                    else:
                        st.error("Please fill out the payment details to authorize the circular economy dispatch order.")
                st.markdown("</div>", unsafe_allow_html=True)True)
            st.markdown("---")
