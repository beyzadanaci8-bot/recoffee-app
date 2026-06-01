import streamlit as st
import pandas as pd
import numpy as np

# Page Layout & Style
st.set_page_config(page_title="ReCoffee - Circular Economy Platform", page_icon="☕", layout="wide")

# Advanced Custom CSS for Modern, Premium App Feel
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * { font-family: 'Poppins', sans-serif; }
    .stApp { background-color: #F9F6F0; }
    
    /* Premium B2B Cards */
    .card {
        background: white;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
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
    
    /* Headers & Text */
    h1, h2, h3 { color: #3E2723 !important; font-weight: 600; }
    .brand-title { font-size: 3rem; font-weight: 700; color: #2E7D32 !important; margin-bottom: 0; }
    .brand-subtitle { font-size: 1.1rem; color: #795548; margin-top: 0; margin-bottom: 30px; }
    
    /* Modern Buttons */
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
    </style>
""", unsafe_allow_html=True)

# State Management Initialization
if 'cafe_waste_balance' not in st.session_state: st.session_state.cafe_waste_balance = 35.0
if 'is_auth' not in st.session_state: st.session_state.is_auth = False
if 'cart_items' not in st.session_state: st.session_state.cart_items = 0

# --- AUTHENTICATION (PROMETHEUS DESIGN) ---
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

# --- PROFESSIONAL DASHBOARD ---
else:
    # Sidebar Professional Navigation Layout
    st.sidebar.markdown("<h2 style='text-align: center; color: #2E7D32 !important;'>ReCoffee Portal</h2>", unsafe_allow_html=True)
    st.sidebar.markdown(f"<p style='text-align: center; color: #795548; font-size: 0.85rem;'>Active Role:<br><b>{st.session_state.role_string}</b></p>", unsafe_allow_html=True)
    st.sidebar.markdown("---")
    
    nav_selection = st.sidebar.radio("Navigation Hub", [
        "🗺️ The Bridge (Live Map & GPS Match)", 
        "🏪 Cafe Portal & Milestones", 
        "🔬 Expert Guidance Page", 
        "🛒 Circular Eco-Market"
    ])
    
    st.sidebar.markdown("---")
    if st.sidebar.button("Secure Logout", use_container_width=True):
        st.session_state.is_auth = False
        st.rerun()

    # SECTION 1: THE BRIDGE (LIVE MAP & RE-DESIGNED LIST)
    if nav_selection == "🗺️ The Bridge (Live Map & GPS Match)":
        st.markdown("<h1>The Bridge: Live Waste Tracker</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #795548;'>Advanced B2B matching ecosystem pairing regional organic waste with verified local producers.</p>", unsafe_allow_html=True)
        
        # Real-time metrics bar
        m1, m2, m3 = st.columns(3)
        total_kg = st.session_state.cafe_waste_balance + 20.0 + 32.0
        m1.metric("Total Available Grounds (İzmir Area)", f"{total_kg:.1f} kg")
        m2.metric("Target SDG Framework Alignment", "SDG 12 & 13")
        m3.metric("Active Environmental Hubs", "3 Hotspots Connected")
        
        st.markdown("### 📍 Live Spatial GPS Mapping (İzmir)")
        # Mocking real GPS coordinates for İzmir Alsancak, Bornova, Urla
        map_df = pd.DataFrame({
            'lat': [38.4385, 38.4633, 38.3244],
            'lon': [27.1432, 27.2167, 26.7644],
            'name': ['Brew Mood Alsancak (15kg ready)', 'Two Cup Bornova (20kg ready)', 'Port Coffee Urla (32kg ready)']
        })
        st.map(map_df, size=15)
        
        # Table Analytics
        st.markdown("### 📊 Nearby Hub Optimization Analytics")
        hotspots_df = pd.DataFrame({
            "Hotspot Location": ["Brew Mood Alsancak", "Two Cup Bornova", "Port Coffee Urla"],
            "Proximity Radius": ["1.2 km", "4.5 km", "12.5 km"],
            "Verified Quantity": [f"{st.session_state.cafe_waste_balance} kg", "20.0 kg", "32.0 kg"],
            "Quality Compliance": ["Premium (Moisture <5%)", "Standard Level", "Pending Lab Verification"]
        })
        st.dataframe(hotspots_df, use_container_width=True)
        st.info("🎯 Location-based parameters automatically minimize logistics routing distances, preventing secondary CO2 emissions.")

    # SECTION 2: CAFE PORTAL & GREEN BADGE MANAGEMENT
    elif nav_selection == "🏪 Cafe Portal & Milestones":
        st.markdown("<h1>Cafe Corporate Portal</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #795548;'>Track your environmental milestones, log volume metrics, and unlock green badges.</p>", unsafe_allow_html=True)
        
        col_p1, col_p2 = st.columns([1.5, 1])
        
        with col_p1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("### 🛡️ 50 kg Trial Rule & Sustainability Milestones")
            current_vol = st.session_state.cafe_waste_balance
            prog = min(current_vol / 50.0, 1.0)
            st.progress(prog)
            
            if current_vol >= 50.0:
                st.success("🎉 **Ecosystem Milestone Reached:** Your establishment has officially unlocked the ReCoffee **'Green Badge'** and a printable physical window sticker with a digital impact tracking QR code!")
            else:
                st.warning(f"🔒 **Status: Standard Partner.** Log exactly **{50.0 - current_vol:.1f} kg** more to secure your verified Green Badge status.")
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Interactive data entry
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

    # SECTION 3: EXPERT AGRICULTURAL GUIDANCE (pH & TIPS)
    elif nav_selection == "🔬 Expert Guidance Page":
        st.markdown("<h1>Expert Consultation & Biological Insights</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #795548;'>B2B expert consulting page for strategic urban crop planning and bio-material analytics.</p>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("### 🧪 Soil Chemistry & pH Matrix")
            st.markdown("<div class='green-accent-box'><b>Average Sample Parameter Range: 5.8 - 6.2 pH</b></div>", unsafe_allow_html=True)
            st.write("Due to nitrogen-dense and mildly acidic compounds, spent grounds are highly optimal for local acidic soil variations in the Aegean region.")
            st.write("🌿 **Highly Compatible Biota:** Citrus variations, local roses, and agricultural blueberry projects.")
            st.markdown("</div>", unsafe_allow_html=True)
            
        with c2:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("### 🪱 Supply Chain Integrity Guidance")
            st.write("1. **Mold Prevention Protocol:** All cafes must dry or isolate damp grounds within **24 hours** from extraction.")
            st.write("2. **Industrial Bio-Fuel Matrix:** Moisture threshold constants must stay **below 5%** to process raw outputs cleanly into pellets.")
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### 📧 Open Portal Inquiry Form")
        st.text_input("Enter Soil Chemistry Specifications or Target Mineral Requirements:")
        st.text_area("Detailed operational inquiry description:")
        if st.button("Submit Inquiry to Agricultural Experts"):
            st.success("Data compiled and dispatched to our agronomy support team. SLA response target within 24 hours.")
        st.markdown("</div>", unsafe_allow_html=True)

    # SECTION 4: THE ECO-MARKETPLACE
    elif nav_selection == "🛒 Circular Eco-Market":
        st.markdown("<h1>The Eco-Marketplace</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #795548;'>Value-based pricing architecture model centered around local circularity and estimated carbon offsets.</p>", unsafe_allow_html=True)
        
        st.sidebar.metric("Shopping Cart", f"{st.session_state.cart_items} Items Added")
        
        market_catalog = [
            {"title": "Premium Bio-Espresso Cup", "origin": "Brew Mood Alsancak", "value": "145 TL", "desc": "100% upcycled structure, heat-resistant casing."},
            {"title": "Nitrogen-Rich Soil Nutrient (2kg)", "origin": "Two Cup Bornova", "value": "80 TL", "desc": "Perfected additive formulation for acidic crops."},
            {"title": "Exfoliating Coffee Body Scrub", "origin": "Coffee Güzelyalı", "value": "110 TL", "desc": "Organic cosmetic material sourced directly from local artisans."},
            {"title": "Eco Bio-Fuel Pellets (Bulk)", "origin": "İzmir Bio-Factory", "value": "220 TL", "desc": "Compressed alternate bio-energy resource for industrial systems."}
        ]
        
        for item in market_catalog:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            cols = st.columns([3, 1])
            with cols[0]:
                st.markdown(f"### {item['title']}")
                st.markdown(f"<p style='color: #2E7D32; font-size: 0.9rem; margin: 0;'><b>Sourced From:</b> {item['origin']}</p>", unsafe_allow_html=True)
                st.write(item['desc'])
            with cols[1]:
                st.markdown(f"<h3 style='text-align: center;'>{item['value']}</h3>", unsafe_allow_html=True)
                if st.button("Add to Batch Order", key=item['title']):
                    st.session_state.cart_items += 1
                    st.toast(f"{item['title']} successfully appended to corporate order configuration!")
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("---")
