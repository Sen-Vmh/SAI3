import streamlit as st
import sys
from pathlib import Path

st.set_page_config(page_title="Finance RAG", layout="centered")

# --- SURVEY STATE ---
if "survey_complete" not in st.session_state:
    st.session_state.survey_complete = False
if "user_profile" not in st.session_state:
    st.session_state.user_profile = {}

# --- CONDITIONAL DISPLAY ---
if not st.session_state.survey_complete:
    st.title("📈 Investment Profile Survey")
    st.write("Before we start, let's understand your current strategy and goals.")
    
    with st.form("survey_form"):
        st.subheader("Basic Information")
        age = st.number_input("How old are you?", min_value=18, max_value=100, value=None, placeholder="Enter age")
        
        st.divider()

        st.subheader("Current Asset Allocation")
        st.caption("What percentage of your portfolio is in each asset class? (must add to 100%)")
        
        c1, c2, c3, c4, c5 = st.columns(5)
        s = c1.number_input("Stocks", 0, 100, value=0)
        b = c2.number_input("Bonds", 0, 100, value=0)
        c = c3.number_input("Cash", 0, 100, value=0)
        r = c4.number_input("Real Estate", 0, 100, value=0)
        cr = c5.number_input("Crypto", 0, 100, value=0)

        c6, c7, c8, c9 = st.columns(4)
        pm = c6.number_input("Precious Metals", 0, 100, value=0)
        etf = c7.number_input("ETFs", 0, 100, value=0)
        hf = c8.number_input("Hedge Funds", 0, 100, value=0)
        other_val = c9.number_input("Other %", 0, 100, value=0)

        custom_other_desc = ""
        if other_val > 0:
            custom_other_desc = st.text_input("Specify 'Other' assets:", placeholder="e.g. Private Equity: 6%, Art: 9%...")

        total_alloc = s + b + c + r + cr + pm + etf + hf + other_val

        if total_alloc == 100:
            st.success(f"Total: {total_alloc}% ✅")
        elif total_alloc > 100:
            st.error(f"Total: {total_alloc}% (Over by {total_alloc - 100}%)")
        else:
            st.info(f"Total: {total_alloc}% (Remaining: {100 - total_alloc}%)")
        
        st.divider()

        st.subheader("Investment Goals")
        
        goal_list = ["Retirement", "Wealth Building", "Passive Income", "Capital Preservation", "Other"]
        
        goal1 = st.selectbox("What is your Primary Investment Goal?", goal_list, index=None)
        custom_goal1 = st.text_input("If 'Other' was selected above, please specify:", key="cg1")

        st.divider()

        st.subheader("Upcoming Major Purchases")
        st.caption("Select all that apply and estimate the cost.")

        purchase_options = [
            "New Car", "Home Down Payment", "Wedding", 
            "Education/Tuition", "Starting a Business", 
            "Major Travel/Sabbatical", "Other"
        ]

        selected_purchases = st.multiselect(
            "What are you saving for in the near future?", 
            purchase_options
        )

        purchase_data = {}

        if selected_purchases:
            st.write("Enter the estimated price or range for each:")
            for item in selected_purchases:
                if item == "Other":
                    c1, c2 = st.columns(2)
                    # Added unique keys for 'Other' to prevent state loss
                    other_name = c1.text_input("What is the other purchase?", placeholder="e.g. Boat", key="other_name_input")
                    other_price = c2.text_input(f"Price for {other_name if other_name else 'Other'}", key="other_price_input")
                    if other_name:
                        purchase_data[other_name] = other_price
                else:
                    # Ensure key is unique per item
                    price = st.text_input(f"Estimated price for {item}", placeholder="e.g. 50,000", key=f"price_{item}")
                    purchase_data[item] = price

        st.divider()

        st.subheader("Investment Concerns & Behavior")
        concern_list = ["Inflation", "Market crash", "Underperforming", "Not saving enough", "Other"]
        concern = st.selectbox("What is your biggest concern about your current portfolio and the future of your investments?", concern_list, index=None)
        custom_concern = st.text_input("If 'Other' was selected above, please specify:", key="cc")
        
        st.divider()

        reaction = st.text_input("How would you feel if your portfolio dropped 30%? If it has happened before, how did it make you feel?", key="reaction")
        
        st.divider()

        rebalance = st.radio("How often do you rebalance your portfolio?", ["Never", "Once a year", "Quarterly", "Monthly"], index=None, horizontal=True)
        last_rebalance = st.text_input("When was the last time you rebalanced?", placeholder="e.g. 3 months ago, never...")
        
        st.divider()
        
        method = st.radio("How do you invest your money?", 
            [
                "Lump sum (Investing large amounts as soon as they are available)", 
                "DCA / Automated (Fixed amount on a regular schedule)", 
                "Opportunistic (Waiting for market dips)",
                "Market Timing (Buying/Selling based on economic predictions)",
                "Dividend Reinvestment (Only growing the portfolio through its own earnings)"
            ], index=None)

        if st.form_submit_button("Complete Profile"):
            check_list = [age, goal1, concern, reaction, rebalance, method, last_rebalance]
            
            missing_basic = any(x is None or x == "" for x in check_list)
            
            # Ensure every selected purchase has a non-empty value in our dict
            missing_purchase_details = any(purchase_data.get(item, "") == "" for item in selected_purchases if item != "Other")
            
            # Check for 'Other'
            if "Other" in selected_purchases:
                other_filled = st.session_state.get("other_name_input") and st.session_state.get("other_price_input")
                if not other_filled:
                    missing_purchase_details = True

            if missing_basic or missing_purchase_details:
                st.error("Please ensure all fields and purchase prices are filled.")
            elif (s+b+c+r+cr+pm+etf+hf+other_val) != 100:
                st.error("Allocation must total 100%.")
            else:
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

else:
    # Put a "Reset" in sidebar so users aren't locked in
    st.sidebar.success("Profile Loaded ✅")

    with st.sidebar.expander("🔍 Your Profile Summary"):
        profile = st.session_state.get("user_profile", {})
        if profile:
            for key, value in profile.items():
                clean_key = key.replace('_', ' ').title()
                if isinstance(value, dict):
                    st.write(f"**{clean_key}:**")
                    for k, v in value.items():
                        st.write(f"  - {k}: {v}")
                else:
                    st.write(f"**{clean_key}:** {value}")

    if st.sidebar.button("Retake Survey"):
        st.session_state.survey_complete = False
        st.rerun()


    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

    from processing.query import ask, build_index, get_collection

    # st.set_page_config(page_title="Finance RAG", layout="centered")
    st.title("Finance RAG")
    st.caption("Ask questions about your financial documents.")


    @st.cache_resource(show_spinner="Loading document index...")
    def load_resources():
        collection = get_collection()
        bm25 = build_index(collection)
        return collection, bm25


    collection, bm25 = load_resources()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant" and "sources" in msg:
                with st.expander("Sources"):
                    for s in msg["sources"]:
                        st.markdown(f"**{s['meta'].get('source', '')}** — {s['meta'].get('headings', '')}")
                        st.caption(s["text"][:300] + "...")

    if question := st.chat_input("What do you want to know?"):
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Searching and generating..."):
                results, answer = ask(question, collection, bm25)
            st.markdown(answer)
            with st.expander("Sources"):
                for s in results:
                    st.markdown(f"**{s['meta'].get('source', '')}** — {s['meta'].get('headings', '')}")
                    st.caption(s["text"][:300] + "...")

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "sources": results,
        })
