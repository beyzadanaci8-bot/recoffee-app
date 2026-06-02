import streamlit as st
import pandas as pd
import time

# 1. ACADEMIC PAGE CONFIGURATION & STYLING
st.set_page_config(
    page_title="ReCoffee - Dokuz Eylül University Faculty of Business", 
    page_icon="☕", 
    layout="wide"
)

# Executive UI/UX Design System Built for Academic Presentations
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    * { font-family: 'Poppins', sans-serif; }
    .stApp { background-color: #FDFBF7; }
    
    /* Academic Executive Cards */
    .card {
        background: white;
        padding: 26px;
        border-radius: 18px;
        box-shadow: 0 4px 25px rgba(0,0,0,0.03);
        margin-bottom: 22px;
        border: 1px solid #EFEBE9;
    }
    .premium-card {
        background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%);
        padding: 26px;
        border-radius: 18px;
        box-shadow: 0 4px 25px rgba(230,124,115,0.12);
        margin-bottom: 22px;
        border: 1px solid #FFB74D;
    }
    .academic-header {
        background: linear-gradient(135deg, #3E2723 0%, #1A0C0A 100%);
        padding: 30px;
        border-radius: 18px;
        color: #F5F5F5 !important;
        margin-bottom: 30px;
        border-left: 8px solid #4CAF50;
    }
    .green-accent-box {
        background-color: #E8F5E9;
        border-left: 5px solid #2E7D32;
        padding: 18px;
        border-radius: 8px;
        margin-bottom: 15px;
    }
    
    /* Typography Overrides */
    h1, h2, h3, h4 { color: #3E2723 !important; font-weight: 600; }
    .brand-title { font-size: 3.2rem; font-weight: 700; color: #2E7D32 !important; margin-bottom: 0; }
    .brand-subtitle { font-size: 1.2rem; color: #795548; margin-top: 0; margin-bottom: 30px; font-style: italic; }
    
    /* Premium Interactive Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);
        color: white;
        border-radius: 25px;
        border: none;
        padding: 12px 35px;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(46, 125, 50, 0.2);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(46, 125, 50, 0.3);
        color: white;
    }
    
    /* Chat Bubble Design */
    .chat-bubble-user { background-color: #EFEBE9; padding: 14px 18px; border-radius: 14px 14px 0 14px; margin-bottom: 12px; text-align: right; color: #3E2723; }
    .chat-bubble-bot { background-color: #E8F5E9; padding: 14px 18px; border-radius: 14px 14px 14px 0; margin-bottom: 22px; border-left: 4px solid #2E7D32; color: #1B5E20; }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 2. APPLICATION STATE MANAGEMENT
# ----------------------------------------------------
if 'cafe_waste_balance' not in st.session_state: st.session_state.cafe_waste_balance = 35.0
if 'producer_collected_waste' not in st.session_state: st.session_state.producer_collected_waste = 45.0
if 'is_premium' not in st.session_state: st.session_state.is_premium = False
if 'is_auth' not in st.session_state: st.session_state.is_auth = False
if 'cart' not in st.session_state: st.session_state.cart = []
if 'expert_chat_history' not in st.session_state: st.session_state.expert_chat_history = []

market_catalog = {
    "Premium Bio-Espresso Cup": {"origin": "Brew Mood Alsancak", "price": 145, "desc": "100% upcycled structure, heat-resistant casing built from localized carbon-offset coffee composite."},
    "Nitrogen-Rich Soil Nutrient (2kg)": {"origin": "Two Cup Bornova", "price": 80, "desc": "Perfected bio-fertiliser additive formulation optimal for soil restoration matrix loops."},
    "Exfoliating Coffee Body Scrub": {"origin": "Coffee Güzelyalı", "price": 110, "desc": "Organic cosmetic consumer goods utilizing antioxidant properties of local grounds extraction."},
    "Eco Bio-Fuel Pellets (Bulk)": {"origin": "İzmir Bio-Factory", "price": 220, "desc": "Compressed alternative energy resource replacing high-emission coal solutions."}
}

# ----------------------------------------------------
# 3. AUTHENTICATION & LOGIN HUB (WITH STRICT INPUT CHECK)
# ----------------------------------------------------
if not st.session_state.is_auth:
    col_l, col_c, col_r = st.columns([0.8, 1.8, 0.8])
    with col_c:
        st.markdown("<div class='card' style='margin-top: 40px; text-align: center;'>", unsafe_allow_html=True)
        st.markdown("<p style='color: #795548; letter-spacing: 2px; font-weight:600; margin-bottom:0;'>MRK 2002 MARKETING APPLICATIONS</p>", unsafe_allow_html=True)
        st.markdown("<h1 class='brand-title' style='margin-top:0;'>ReCoffee</h1>", unsafe_allow_html=True)
        st.markdown("<p class='brand-subtitle'>\"Your morning coffee, changed.\"</p>", unsafe_allow_html=True)
        
        email_inp = st.text_input("Corporate / Stakeholder Email", placeholder="example@deu.edu.tr")
        pass_inp = st.text_input("Security Key Access", type="password", placeholder="••••••••")
        user_role_inp = st.selectbox("Select Your User Ecosystem Profile", [
            "Cafe / Coffee Shop (Waste Supplier)", 
            "Producer / Manufacturer (Waste Recycler)"
        ])
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Initialize Circular Ecosystem Bridge", use_container_width=True):
            # 🔥 STRICT VALIDATION CORE: Giriş alanlarının doluluk kontrolü
            if not email_inp.strip() and not pass_inp.strip():
                st.error("🔒 **Access Denied:** Email and Security Key areas cannot be left entirely blank. Please provide corporate credentials to bridge into the system.")
            elif not email_inp.strip():
                st.error("📧 **Access Denied:** Corporate Email field is empty. Input a verified email token.")
            elif "@" not in email_inp or "." not in email_inp:
                st.error("⚠️ **Access Denied:** Invalid corporate email structure pattern. Please check and format correctly (e.g., node@recoffee.com).")
            elif not pass_inp.strip():
                st.error("🔑 **Access Denied:** Security Key parameter missing. Input your cluster access key.")
            else:
                # All controls passed successfully
                st.session_state.is_auth = True
                st.session_state.role_string = user_role_inp
                st.rerun()
            
        st.markdown("""
            <p style='font-size:0.8rem; color:#A1887F; margin-top:20px;'>
            <b>Project Group:</b> Beyzanur Danacı, Büşra Fadime Ayan, Ayça Biçer, Sıla Zerger<br>
            Dokuz Eylül University Faculty of Business Administration — 2026
            </p>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------
# 4. MAIN EXECUTIVE APPLICATION HUB (ROLE-BASED)
# ----------------------------------------------------
else:
    # Sidebar Setup
    st.sidebar.markdown("<h2 style='text-align: center; color: #2E7D32 !important; margin-bottom:5px;'>ReCoffee Hub</h2>", unsafe_allow_html=True)
    
    if st.sidebar.button("Secure Logout", use_container_width=True):
        st.session_state.is_auth = False
        st.session_state.cart = []
        st.rerun()
        
    st.sidebar.markdown("---")
    
    # ----------------------------------------------------
    # ROLE 1: CAFE USER INTERFACE
    # ----------------------------------------------------
    if st.session_state.role_string == "Cafe / Coffee Shop (Waste Supplier)":
        st.sidebar.markdown("<div style='text-align: center; color: #795548; font-size: 0.85rem; margin-bottom:15px; padding: 8px; background:#E8F5E9; border-radius:8px; border: 1px solid #C8E6C9; color:#1B5E20;'><b>Logged in as:</b><br>☕ Waste Supplier Node</div>", unsafe_allow_html=True)
        
        cafe_nav = st.sidebar.radio("Navigation Hub", [
            "🏪 Cafe Portal & Milestones",
            "🔬 Material Science Guidance",
            "🛒 Circular Eco-Market"
        ])
        
        if cafe_nav == "🏪 Cafe Portal & Milestones":
            st.markdown("""
                <div class='academic-header'>
                    <h2 style='color:white !important; margin:0;'>Cafe Management & Sustainability Milestones</h2>
                    <p style='color:#A5D6A7 !important; margin:5px 0 0 0;'>Track environmental benchmarks, dispatch metrics, and unlock green validation certificates.</p>
                </div>
            """, unsafe_allow_html=True)
            
            col_cp1, col_cp2 = st.columns([1.6, 1])
            with col_cp1:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown("### 🛡️ 50 kg Trial Quota Milestone Tracker")
                current_vol = st.session_state.cafe_waste_balance
                progress_factor = min(current_vol / 50.0, 1.0)
                st.progress(progress_factor)
                
                if current_vol >= 50.0:
                    st.success("🎉 **Green Badge Unlocked!** Your establishment has reached the 50kg benchmark. Your store's storefront QR impact sticker is authorized for deployment[cite: 1, 2].")
                else:
                    st.warning(f"💡 You need to dispatch exactly **{50.0 - current_vol:.1f} kg** more coffee grounds to claim your verified 'Green Badge'[cite: 1, 2].")
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown("### 📈 Log Daily Waste Dispatch")
                new_metric = st.number_input("Input Coffee Grounds Weight Metric to Log (kg):", min_value=0.0, step=1.0, value=0.0)
                if st.button("Confirm Dispatch Authorization", use_container_width=True):
                    st.session_state.cafe_waste_balance += new_metric
                    st.success(f"Ecosystem ledger updated! Routed {new_metric} kg into the circular chain.")
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
                
            with col_cp2:
                st.markdown("<div class='card' style='text-align:center;'>", unsafe_allow_html=True)
                st.markdown("### 🏅 Verified Credential Status")
                if st.session_state.cafe_waste_balance >= 50.0:
                    st.markdown("<p style='font-size:5.5rem; margin:0;'>🟢</p>", unsafe_allow_html=True)
                    st.markdown("<h4 style='color:#2E7D32 !important; margin:0;'>GREEN BADGE COMPLIANT</h4><p style='font-size:0.85rem; color:#795548;'>CSR corporate target validation active. Customer trust matrix accelerated[cite: 1, 2].</p>", unsafe_allow_html=True)
                else:
                    st.markdown("<p style='font-size:5.5rem; margin:0;'>🟡</p>", unsafe_allow_html=True)
                    st.markdown("<h4 style='color:#E65100 !important; margin:0;'>STANDARD TIER</h4><p style='font-size:0.85rem; color:#795548;'>Increase your baseline circular volume contribution to unlock partner validation criteria[cite: 1, 2].</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

    # ----------------------------------------------------
    # ROLE 2: PRODUCER INTERFACE (HYBRID PRICING)
    # ----------------------------------------------------
    elif st.session_state.role_string == "Producer / Manufacturer (Waste Recycler)":
        st.sidebar.markdown("<div style='text-align: center; color: #795548; font-size: 0.85rem; margin-bottom:15px; padding: 8px; background:#FFF3E0; border-radius:8px; border: 1px solid #FFE0B2; color:#E65100;'><b>Logged in as:</b><br>🚜 Waste Recycler Node</div>", unsafe_allow_html=True)
        
        prod_nav = st.sidebar.radio("Navigation Hub", [
            "🗺️ The Bridge (Sourcing Map)", 
            "💎 Premium Subscription & Quota Engine",
            "🔬 Agronomy Consultation & Q&A Portal", 
            "🛒 Eco-Marketplace"
        ])
        
        if prod_nav == "🗺️ The Bridge (Sourcing Map)":
            st.markdown("""
                <div class='academic-header'>
                    <h2 style='color:white !important; margin:0;'>The Bridge: Live Sourcing Tracker</h2>
                    <p style='color:#A5D6A7 !important; margin:5px 0 0 0;'><b>Place Strategy Framework:</b> B2B Matching Optimization Module via Spatial GPS Parameters[cite: 1, 2].</p>
                </div>
            """, unsafe_allow_html=True)
            
            if not st.session_state.is_premium and st.session_state.producer_collected_waste >= 60.0:
                st.error("🔒 **B2B Sourcing Interface Locked!** Your enterprise profile has exhausted its free threshold allocation limit (60 kg). Sourcing continuous material now requires a **50 TL/month Base Subscription Token** + **1 TL/kg surcharge parameters**[cite: 1, 2]. Please access the Quota Engine to unlock.")
            else:
                m1, m2, m3 = st.columns(3)
                current_total_pool = st.session_state.cafe_waste_balance + 20.0 + 32.0
                m1.metric("Total Available Grounds (İzmir Area)", f"{current_total_pool:.1f} kg")
                m2.metric("Target Pricing Model", "Hybrid Surcharge Architecture[cite: 1, 2]")
                m3.metric("Active Environmental Hubs", "3 Hotspots Connected[cite: 1, 2]")
                
                st.markdown("### 📍 Spatial GPS Matching Cluster")
                map_df = pd.DataFrame({
                    'lat': [38.4385, 38.4633, 38.3244],
                    'lon': [27.1432, 27.2167, 26.7644],
                    'name': ['Brew Mood Alsancak (15kg)', 'Two Cup Bornova (20kg)', 'Port Coffee Urla (32kg)']
                })
                st.map(map_df, size=16)
                
                st.markdown("### 📋 Spatial Hub Analytical Metrics Matrix")
                hotspots_df = pd.DataFrame({
                    "Ecosystem Node Location": ["Brew Mood Alsancak Hub", "Two Cup Bornova Hub", "Port Coffee Urla Hub"],
                    "Proximity Radius Boundary": ["1.2 km Cluster", "4.5 km Cluster", "12.5 km Cluster"],
                    "Verified Available Volume": [f"{st.session_state.cafe_waste_balance} kg", "20.0 kg", "32.0 kg"],
                    "Strategic Baseline Cost": ["0 TL (Below 60kg Threshold)[cite: 1, 2]", "0 TL", "0 TL"]
                })
                st.dataframe(hotspots_df, use_container_width=True)

        elif prod_nav == "💎 Premium Subscription & Quota Engine":
            st.markdown("""
                <div class='academic-header'>
                    <h2 style='color:white !important; margin:0;'>B2B Hybrid Pricing Engine</h2>
                    <p style='color:#A5D6A7 !important; margin:5px 0 0 0;'><b>Pricing Model Configuration:</b> Fixed 50 TL/Month Subscription Matrix + 1 TL/kg Scaled Variable Cost Parameter Above 60kg Quota[cite: 1, 2].</p>
                </div>
            """, unsafe_allow_html=True)
            
            col_rev1, col_rev2 = st.columns([1.5, 1])
            with col_rev1:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown("### 📊 Enterprise Sourcing Ledger Metrics")
                collected = st.session_state.producer_collected_waste
                st.markdown(f"Your factory profile has extracted a cumulative: <b style='font-size:1.3rem; color:#2E7D32;'>{collected:.1f} kg</b> from localized clusters.", unsafe_allow_html=True)
                
                st.markdown("#### 💳 Financial Billing Allocation Breakdown:")
                base_sub_fee = 50 if st.session_state.is_premium else 0
                
                if collected > 60.0:
                    surcharge_kg = collected - 60.0
                    variable_fee = surcharge_kg * 1.0
                else:
                    surcharge_kg = 0
                    variable_fee = 0
                    
                total_invoice = base_sub_fee + variable_fee
                
                c_led1, c_led2 = st.columns(2)
                c_led1.write(f"• Fixed Base Monthly Subscription Fee:")
                c_led2.write(f"**{base_sub_fee} TL**")
                c_led1.write(f"• Surcharge Volume Parameter (> 60 kg limit):")
                c_led2.write(f"**{surcharge_kg:.1f} kg**")
                c_led1.write(f"• Variable Surcharge Cost Allocation (1 TL / kg):")
                c_led2.write(f"**{variable_fee:.1f} TL**")
                st.markdown("---")
                st.markdown(f"##### 🧾 Current Aggregated Monthly Statement Due: <b style='color:#E65100; font-size:1.2rem;'>{total_invoice:.1f} TL</b>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown("### 🚜 Simulate B2B Sourcing Stream Extraction")
                sim_add = st.number_input("Designate Volume to Squeeze From Active Nodes (kg):", min_value=0.0, step=5.0, value=10.0)
                if st.button("Execute Extraction Over The Bridge"):
                    if not st.session_state.is_premium and (st.session_state.producer_collected_waste + sim_add) >= 60.0:
                        st.error("❌ **Transaction Refused:** This operation will push your allocation over the 60 kg ceiling barrier. You must activate the 50 TL/Month Premium Subscription tier to authorize this transaction[cite: 1, 2].")
                    else:
                        st.session_state.producer_collected_waste += sim_add
                        st.toast(f"Logged {sim_add} kg of industrial resource materials!")
                        st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
                
            with col_rev2:
                st.markdown("<div class='premium-card' style='text-align: center;'>", unsafe_allow_html=True)
                st.markdown("<p style='color: #E65100; letter-spacing: 1px; font-weight:600; font-size:0.8rem; margin:0;'>HYBRID SUBSCRIPTION HUB</p>", unsafe_allow_html=True)
                st.markdown("<h3 style='margin-top:5px;'>👑 Premium B2B Tier</h3>", unsafe_allow_html=True)
                st.markdown("<h1 style='color:#E65100 !important; font-size:3rem; margin:10px 0;'>50 TL <span style='font-size:1rem; color:#795548; font-weight:400;'>/ month</span></h1>", unsafe_allow_html=True)
                st.markdown("<p style='font-size:0.85rem; color:#5D4037;'><b>+ 1 TL per additional kg</b> extracted once your enterprise passes the 60 kg operational boundary[cite: 1, 2].</p>", unsafe_allow_html=True)
                st.markdown("---")
                st.markdown("""
                    <div style='text-align:left; font-size:0.82rem; color:#5D4037; line-height:1.6; margin-bottom:15px;'>
                    🔓 <b>Complete Spatial GPS Map Integration</b><br>
                    🚀 <b>Bypass Authority over the 60kg Limit Ceiling</b><br>
                    🏭 <b>Scalable Sourcing Configurations for Industrial Needs</b>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.session_state.is_premium:
                    if st.button("Deactivate Premium License Token", use_container_width=True):
                        st.session_state.is_premium = False
                        st.session_state.producer_collected_waste = 45.0
                        st.rerun()
                else:
                    if st.button("Authorize 50 TL Premium Subscription", use_container_width=True):
                        st.session_state.is_premium = True
                        st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

    # ----------------------------------------------------
    # MUTUAL COMMODITY SECTIONS AVAILABLE TO ALL
    # ----------------------------------------------------
    if nav_selection == "🔬 Material Science Guidance" or (st.session_state.role_string == "Producer / Manufacturer (Waste Recycler)" and prod_nav == "🔬 Agronomy Consultation & Q&A Portal"):
        st.markdown("<div class='academic-header'><h2>Expert Consultation & Applied Material Science</h2></div>", unsafe_allow_html=True)
        col_ag1, col_ag2 = st.columns(2)
        with col_ag1:
            st.markdown("<div class='card'><h3>🧪 Soil Chemistry Optimization</h3><p><b>Optimal Range: 5.8 - 6.2 pH Range</b><br>Highly compatible for regional citrus vegetation and roses.</p></div>", unsafe_allow_html=True)
        with col_ag2:
            st.markdown("<div class='card'><h3>🪱 Quality Control Parameters</h3><p>• Mold Isolation: Dry grounds within <b>24 hours</b>.<br>• Bio-Fuel Pellets: Maintain moisture parameters <b>under 5%</b>.</p></div>", unsafe_allow_html=True)
            
        st.markdown("### 💬 Live Interactive Consultation Interface")
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        for chat in st.session_state.expert_chat_history:
            if chat['role'] == 'user': st.markdown(f"<div class='chat-bubble-user'><b>You:</b> {chat['text']}</div>", unsafe_allow_html=True)
            else: st.markdown(f"<div class='chat-bubble-bot'><b>Agronomist AI Engine:</b> {chat['text']}</div>", unsafe_allow_html=True)
        
        user_query = st.text_input("Input customized agronomy or substrate query:")
        if st.button("Transmit Query Token"):
            if user_query:
                st.session_state.expert_chat_history.append({'role': 'user', 'text': user_query})
                resp = "Spent coffee grounds are highly rich in essential nitrogen minerals. Since properties track at 5.8-6.2 pH, configure deployment primarily around acid-loving regional crops."
                if "mushroom" in user_query.lower(): resp = "Oyster mushrooms display high yield trends when grown on pasteurized spent coffee ground substrates due to nitrogen availability parameters."
                st.session_state.expert_chat_history.append({'role': 'bot', 'text': resp})
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    elif nav_selection == "🛒 Circular Eco-Market" or (st.session_state.role_string == "Producer / Manufacturer (Waste Recycler)" and prod_nav == "🛒 Eco-Marketplace"):
        st.markdown("<div class='academic-header'><h2>Upcycled Commercial Eco-Marketplace</h2></div>", unsafe_allow_html=True)
        col_mk1, col_mk2 = st.columns([1.8, 1])
        with col_mk1:
            for title, info in market_catalog.items():
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                cols = st.columns([3, 1])
                cols[0].markdown(f"#### {title}")
                cols[0].markdown(f"<p style='color: #2E7D32; font-size: 0.85rem; margin: 0;'><b>Supply Node:</b> {info['origin']}</p>", unsafe_allow_html=True)
                cols[0].write(info['desc'])
                cols[1].markdown(f"<h3 style='text-align: center; margin-top:12px;'>{info['price']} TL</h3>", unsafe_allow_html=True)
                if cols[1].button("Append to Batch", key=title):
                    st.session_state.cart.append({"title": title, "price": info['price']})
                    st.toast(f"{title} appended into configuration matrix!")
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
        with col_mk2:
            st.markdown("### 🛒 Order Configuration Matrix")
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            if not st.session_state.cart:
                st.write("*Cart contains zero active lines.*")
                total_price = 0
            else:
                total_price = 0
                for item in st.session_state.cart:
                    st.write(f"• {item['title']} — {item['price']} TL")
                    total_price += item['price']
                st.markdown("---")
                st.markdown(f"#### **Total Due: {total_price} TL**")
                if st.button("Flush Order Configuration"):
                    st.session_state.cart = []
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
            
            if total_price > 0:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown("#### 💳 Secure Settlement Gateway")
                st.text_input("Cardholder Name")
                st.text_input("Card Number", max_chars=19)
                if st.button("Authorize Payment Protocol"):
                    st.success(f"🎉 Electronic Financial Settlement Confirmed! Payment of {total_price} TL cleared.")
                    st.session_state.cart = []
                st.markdown("</div>", unsafe_allow_html=True)
