import streamlit as st

def render_survey():

    # 1. Initialize session state for validation and profile
    if "show_errors" not in st.session_state:
        st.session_state.show_errors = False
    if "survey_complete" not in st.session_state:
        st.session_state.survey_complete = False
    if "user_profile" not in st.session_state:
        st.session_state.user_profile = None

    #helper fuction to highlight missing fields
    def req(label, key):
        if st.session_state.show_errors:
            val = st.session_state.get(key)
            if val is None or val == "" or val == []:
                return f"{label} :red[*(Required)]"
        return label

    st.title("📈 Investment Profile Survey")
    st.write("Before we start, let's understand your current strategy and goals.")
    
    if st.button("autofill"):
        st.session_state.user_profile = {
            "age": 29,
            "primary_goal": "Build long-term wealth",
            "major_purchases": {
                "house": {"timeline": "5–7 years", "budget": 650000},
                "car": {"timeline": "2 years", "budget": 30000},
                "education": None,
                "other": None
            },
            "concern": "Market volatility",
            "risk_reaction": "I get nervous but usually stay invested",
            "investing_method": "Automated monthly contributions",
            "rebalance_freq": "Quarterly",
            "last_rebalanced": "2025-12-15",
            "allocation": (
                "Stocks:55%, Bonds:20%, Cash:5%, RE:10%, Crypto:5%, "
                "PM:2%, ETFs:2%, HF:0%, Other:1% (Angel investments)"
            )
        }

        st.session_state.survey_complete = True
        st.rerun()

    # --- BASIC INFO --- 
    st.subheader("Basic Information")
    age = st.number_input(req("How old are you?", "age"), min_value=18, max_value=100, value=None, placeholder="Enter age", key="age")

    
    st.divider()

    # --- ASSET ALLOCATION ---
    st.subheader("Current Asset Allocation")
    st.caption("What percentage of your portfolio is in each asset class? (must add to 100%)")
    
    c1, c2, c3, c4, c5 = st.columns(5)
    s = c1.number_input("Stocks", 0, 100, value=0, key="s")
    b = c2.number_input("Bonds", 0, 100, value=0, key="b")
    c = c3.number_input("Cash", 0, 100, value=0, key="c")
    r = c4.number_input("Real Estate", 0, 100, value=0, key="r")
    cr = c5.number_input("Crypto", 0, 100, value=0, key="cr")

    c6, c7, c8, c9 = st.columns(4)
    pm = c6.number_input("Precious Metals", 0, 100, value=0, key="pm")
    etf = c7.number_input("ETFs", 0, 100, value=0, key="etf")
    hf = c8.number_input("Hedge Funds", 0, 100, value=0, key="hf")
    other_val = c9.number_input("Other %", 0, 100, value=0, key="other_val")

    # --- LIVE UPDATE: Other Assets Description ---
    custom_other_desc = ""
    if other_val > 0:
        other_desc_label = req("Specify 'Other' assets:", "other_desc")
        custom_other_desc = st.text_input(other_desc_label, placeholder="e.g. Private Equity: 6%, Art: 9%...", key="other_desc")

    total_alloc = s + b + c + r + cr + pm + etf + hf + other_val

    if total_alloc == 100:
        st.success(f"Total: {total_alloc}% ✅")
    elif st.session_state.show_errors or total_alloc > 100:
        st.error(f"Total: {total_alloc}% — :red[Must equal exactly 100%]")
    else:
        st.info(f"Total: {total_alloc}% (Remaining: {100 - total_alloc}%)")
    
    st.divider()

    # --- GOALS
    st.subheader("Investment Goals")
    
    goal_list = ["Retirement", "Wealth Building", "Passive Income", "Capital Preservation", "Other"]
    
    goal1 = st.selectbox(req("What is your Primary Investment Goal?", "goal1"), goal_list, index=None, key="goal1")
    if goal1 == "Other":
        custom_goal1 = st.text_input(req("Please specify your goal:", "cg1"), key="cg1")
    else:
        custom_goal1 = ""
    st.divider()

    # --- PURCHASES ---
    st.subheader("Upcoming Major Purchases")
    st.caption("Select all that apply and estimate the cost.")

    purchase_options = [
        "New Car", "Home Down Payment", "Wedding", 
        "Education/Tuition", "Starting a Business", 
        "Major Travel/Sabbatical", "Other"
    ]

    selected_purchases = st.multiselect(req(
        "What are you saving for in the near future?", "selected_purchases"), 
        purchase_options,
        key="selected_purchases"
    )

    purchase_data = {}

    if selected_purchases:
        st.write("Enter the estimated price or range for each:")
        for item in selected_purchases:
            if item == "Other":
                c1, c2 = st.columns(2)
                # Added unique keys for 'Other' to prevent state loss
                other_name_label = req("What is the other purchase?", "other_name_input")
                other_name = c1.text_input(other_name_label, placeholder="e.g. Boat", key="other_name_input")
                
                other_price_label = req(f"Price for {other_name if other_name else 'Other'}", "other_price_input")
                other_price = c2.text_input(other_price_label, key="other_price_input")
                
                if other_name:
                    purchase_data[other_name] = other_price
            else:
                # Ensure key is unique per item
                price_label = req(f"Estimated price for {item}", f"price_{item}")
                price = st.text_input(price_label, placeholder="e.g. 50,000", key=f"price_{item}")
                purchase_data[item] = price

    st.divider()

    # --- CONCERNS & BEHAVIOR ---
    st.subheader("Investment Concerns & Behavior")

    concern_list = ["Inflation", "Market crash", "Underperforming", "Not saving enough", "Other"]
    concern = st.selectbox(req("What is your biggest concern about your current portfolio and the future of your investments?", "concern"), concern_list, index=None, key="concern")
    
    if concern == "Other":
        custom_concern = st.text_input(req("Please specify your concern:", "cc"), key="cc")
    else:
        custom_concern = ""    

    st.divider()

    reaction = st.text_input(req("How would you feel if your portfolio dropped 30%? If it has happened before, how did it make you feel?", "reaction"), key="reaction")
    
    st.divider()

    rebalance = st.radio(req("How often do you rebalance your portfolio?", "rebalance"), ["Never", "Once a year", "Quarterly", "Monthly"], index=None, horizontal=True, key="rebalance")
    last_rebalance = st.text_input(req("When was the last time you rebalanced?", "last_rebalance"), placeholder="e.g. 3 months ago, never...", key="last_rebalance")
    
    st.divider()
    
    method = st.radio(req("How do you invest your money?", "method"), 
        [
            "Lump sum (Investing large amounts as soon as they are available)", 
            "DCA / Automated (Fixed amount on a regular schedule)", 
            "Opportunistic (Waiting for market dips)",
            "Market Timing (Buying/Selling based on economic predictions)",
            "Dividend Reinvestment (Only growing the portfolio through its own earnings)"
        ], index=None, key="method")

#--- SUBMIT & VALIDATION ---
    if st.button("Complete Profile"):
        # 1. Base keys
        required_keys = ["age", "goal1", "concern", "reaction", "rebalance", "last_rebalance", "method"]
        
        # 2. Conditional 'Other' keys
        if st.session_state.get("other_val", 0) > 0:
            required_keys.append("other_desc")
        if st.session_state.get("goal1") == "Other":
            required_keys.append("cg1")
        if st.session_state.get("concern") == "Other":
            required_keys.append("cc")

        missing_basic = any(not st.session_state.get(k) for k in required_keys)            
        # Ensure every selected purchase has a non-empty value in our dict
        missing_purchase_details = any(purchase_data.get(item, "") == "" for item in selected_purchases if item != "Other")
        
        # Check for 'Other'
        if "Other" in selected_purchases:
            if not st.session_state.get("other_name_input") or not st.session_state.get("other_price_input"):
                missing_purchase_details = True

        if missing_basic or missing_purchase_details:
            st.session_state.show_errors = True
            st.error("Please ensure all fields and purchase prices are filled.")
            st.rerun()
        elif (s+b+c+r+cr+pm+etf+hf+other_val) != 100:
            st.error("Allocation must total 100%.")
        else:
            st.session_state.show_errors = False
            st.session_state.user_profile = {
                "age": age, 
                "primary_goal": custom_goal1 if goal1 == "Other" else goal1, 
                "major_purchases": purchase_data, # This will now contain the data
                "concern": custom_concern if concern == "Other" else concern, 
                "risk_reaction": reaction, 
                "investing_method": method,
                "rebalance_freq": rebalance,
                "last_rebalanced": last_rebalance,
                "allocation": f"Stocks:{s}%, Bonds:{b}%, Cash:{c}%, RE:{r}%, Crypto:{cr}%, PM:{pm}%, ETFs:{etf}%, HF:{hf}%, Other:{other_val}% ({custom_other_desc})"
            }
            st.session_state.survey_complete = True
            st.rerun()

    if st.session_state.show_errors:
        st.error("Please ensure all fields marked with :red[*(Required)] are filled and allocation totals 100%.")

