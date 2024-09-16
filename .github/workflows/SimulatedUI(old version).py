#James Anatole UI for simulated
import pandas as pd
import random
import streamlit as st

# Where User starts of with - link to other pages
def landing_page():
    st.title("Trading Game Simulated")
    st.header("Welcome to the Trading Game Simulated")
    st.subheader("A Blackhelm Equity Project") #TBD

    st.write("## Features Overview")
    st.write("- **Order Placement:** Place buy and sell orders at various prices")
    st.write("- **Algorithmic Trading:** Enable low-code algorithms for automated trading")
    st.write("- **Bot Trading:** Select number of bots and their trading frequency")
    st.write("- **Macro Events:** Influence stock prices with macro events")

    st.write("### Footer")
    st.write("{link to blackhelm contact} | {link to blackhelm instagram} | {link to blackhelm linkedIN}") #TBD

def dashboard():
    st.title("Dashboard")
    st.sidebar.title("Navigation")
    st.sidebar.write("Dashboard")
    st.sidebar.write("Place Order")
    st.sidebar.write("Algorithmic Trading")
    st.sidebar.write("Bot Trading")
    st.sidebar.write("PnL History")
    st.sidebar.write("Settings")

    st.write("### Market Overview")
    st.line_chart({"Stock Prices": [100, 105, 102, 108, 110]})

    st.write("### PnL Summary")
    st.write("Profit and Loss: $500")

    st.write("### Recent Orders")
    st.table({"Order ID": [1, 2, 3], "Type": ["Buy", "Sell", "Buy"], "Status": ["Completed", "Pending", "Completed"]})

    st.write("### Macro Events")
    st.write("Upcoming Events: Federal Reserve Meeting")

def order_placement_page():
    st.title("Place Order")
    st.sidebar.title("Navigation")
    st.sidebar.write("Dashboard")
    st.sidebar.write("Place Order")
    st.sidebar.write("Algorithmic Trading")
    st.sidebar.write("Bot Trading")
    st.sidebar.write("PnL History")
    st.sidebar.write("Settings")

    st.write("### Order Form")
    order_type = st.selectbox("Order Type", ["Buy", "Sell"])
    stock = st.selectbox("Stock", ["AAPL", "GOOGL", "MSFT"])
    price = st.number_input("Price")
    quantity = st.number_input("Quantity")
    st.button("Place Order")

    st.write("### Order Book")
    st.write("#### Buy Orders")
    st.table({"Order ID": [1, 2], "Stock": ["AAPL", "GOOGL"], "Price": [150, 120], "Quantity": [10, 5]})

    st.write("#### Sell Orders")
    st.table({"Order ID": [3, 4], "Stock": ["MSFT", "AAPL"], "Price": [110, 160], "Quantity": [8, 2]})

def algorithmic_trading_page():
    st.title("Algorithmic Trading")
    st.sidebar.title("Navigation")
    st.sidebar.write("Dashboard")
    st.sidebar.write("Place Order")
    st.sidebar.write("Algorithmic Trading")
    st.sidebar.write("Bot Trading")
    st.sidebar.write("PnL History")
    st.sidebar.write("Settings")

    st.write("### Algorithm Editor")
    code = st.text_area("Write your algorithm here")
    st.button("Run")
    st.button("Save")

    st.write("### Trading Bots")
    bot_count = st.number_input("Number of Bots", 1, 10)
    frequency = st.selectbox("Trading Frequency", ["Every minute", "Hourly", "Daily"])
    st.write(f"Currently running {bot_count} bots with {frequency} frequency.")

def pnl_history_page():
    st.title("PnL and Order History")
    st.sidebar.title("Navigation")
    st.sidebar.write("Dashboard")
    st.sidebar.write("Place Order")
    st.sidebar.write("Algorithmic Trading")
    st.sidebar.write("Bot Trading")
    st.sidebar.write("PnL History")
    st.sidebar.write("Settings")

    st.write("### PnL Chart")
    st.line_chart({"PnL": [500, 520, 510, 530, 540]})

    st.write("### Order History")
    st.table({"Order ID": [1, 2, 3], "Type": ["Buy", "Sell", "Buy"], "Status": ["Completed", "Pending", "Completed"], "Price": [150, 120, 110], "Quantity": [10, 5, 8]})

def bot_trading_page():
    st.title("Bot Trading")
    st.sidebar.title("Navigation")
    st.sidebar.write("Dashboard")
    st.sidebar.write("Place Order")
    st.sidebar.write("Algorithmic Trading")
    st.sidebar.write("Bot Trading")
    st.sidebar.write("PnL History")
    st.sidebar.write("Settings")

    st.write("### Bot Settings")
    bot_count = st.number_input("Number of Bots", 1, 10)
    frequency = st.selectbox("Trading Frequency", ["Every minute", "Hourly", "Daily"])

    st.write("### Bot Performance")
    st.table({"Bot ID": [1, 2], "PnL": [100, 150], "Success Rate": ["70%", "80%"]})

def macro_events_page():
    st.title("Macro Events")
    st.sidebar.title("Navigation")
    st.sidebar.write("Dashboard")
    st.sidebar.write("Place Order")
    st.sidebar.write("Algorithmic Trading")
    st.sidebar.write("Bot Trading")
    st.sidebar.write("PnL History")
    st.sidebar.write("Settings")

    st.write("### Events Calendar")
    st.write("Augsut 2024: Federal Reserve Meeting")
    st.write("November 2024: GDP Report Release")

    st.write("### Event Details")
    st.write("Federal Reserve Meeting: Discussion on potential interest rate changes which could affect market volatility.")

# Streamlit app main function
def main():
    st.sidebar.title("Trading Game Simulated")
    page = st.sidebar.selectbox("Choose a page", ["Landing Page", "Dashboard", "Place Order", "Algorithmic Trading", "PnL History", "Bot Trading", "Macro Events"])

    if page == "Landing Page":
        landing_page()
    elif page == "Dashboard":
        dashboard()
    elif page == "Place Order":
        order_placement_page()
    elif page == "Algorithmic Trading":
        algorithmic_trading_page()
    elif page == "PnL History":
        pnl_history_page()
    elif page == "Bot Trading":
        bot_trading_page()
    elif page == "Macro Events":
        macro_events_page()

if __name__ == "__main__":
    main()