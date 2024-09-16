import streamlit as st
import pandas as pd
import random

# volatile hold for when running - store to a db later on 
order_book = {"buy": [], "sell": []}
executed_orders = []
bot_strategies = []
macro_events = [{"date": "August 2024", "event": "Blackhelm Meeting ", "impact": "Volatility"}]  #Example Layout

def match_orders():
    """
    Match buy and sell orders based on price-time priority.
    Executes trades and updates the order book.
    """
    global order_book, executed_orders
    # Sort orders by price and then by time (FIFO)
    buy_orders = sorted(order_book["buy"], key=lambda x: (-x['price'], x['time']))
    sell_orders = sorted(order_book["sell"], key=lambda x: (x['price'], x['time']))
    
    while buy_orders and sell_orders and buy_orders[0]['price'] >= sell_orders[0]['price']:
        buy_order = buy_orders.pop(0)
        sell_order = sell_orders.pop(0)
        
        # Execute trade
        trade_quantity = min(buy_order['quantity'], sell_order['quantity'])
        executed_orders.append({
            "buy_id": buy_order['id'], 
            "sell_id": sell_order['id'], 
            "price": sell_order['price'], 
            "quantity": trade_quantity
        })
        
        # Update remaining quantities or remove the order if fully executed
        if buy_order['quantity'] > trade_quantity:
            buy_order['quantity'] -= trade_quantity
            buy_orders.insert(0, buy_order)  # Reinsert with updated quantity
        if sell_order['quantity'] > trade_quantity:
            sell_order['quantity'] -= trade_quantity
            sell_orders.insert(0, sell_order)  # Reinsert with updated quantity

    # Update the global order book
    order_book['buy'] = buy_orders
    order_book['sell'] = sell_orders

def add_order(order_type, stock, price, quantity):
    """
    Add a new order to the order book and attempt to match it.
    """
    global order_book
    order = {
        "id": len(order_book[order_type]) + 1,
        "stock": stock,
        "price": price,
        "quantity": quantity,
        "time": st.time()
    }
    order_book[order_type].append(order)
    match_orders()

def execute_bot_trading():
    """
    Execute trading strategies for bots at predefined intervals.
    """
    global bot_strategies, order_book
    for bot in bot_strategies:
        # Randomly decide whether the bot buys or sells
        order_type = random.choice(["buy", "sell"])
        stock = random.choice(["AAPL", "GOOGL", "MSFT"])
        price = random.uniform(100, 200)
        quantity = random.randint(1, 10)
        add_order(order_type, stock, price, quantity)

def adjust_prices_for_macro_events():
    """
    Adjust stock prices based on macro events.
    """
    global macro_events
    # Example impact: Increase or decrease all stock prices by a random percentage
    impact_factor = random.uniform(-0.05, 0.05)
    stock_prices = {"AAPL": 150, "GOOGL": 120, "MSFT": 100}
    for stock in stock_prices:
        stock_prices[stock] *= (1 + impact_factor)
    return stock_prices

def landing_page():
    st.title("Trading Game Simulated")
    st.header("Welcome to the Trading Game Simulated")
    st.subheader("A Blackhelm Equity Project")
    if st.button("Get Started"):
        st.session_state["page"] = "Dashboard"
    
    st.write("## Features Overview")
    st.write("- **Order Placement:** Place buy and sell orders at various prices")
    st.write("- **Algorithmic Trading:** Enable low-code algorithms for automated trading")
    st.write("- **Bot Trading:** Select number of bots and their trading frequency")
    st.write("- **Macro Events:** Influence stock prices with macro events")

    st.write("### Footer")
    st.write("{link to blackhelm contact} | {link to blackhelm instagram} | {link to blackhelm linkedIN}")

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
    stock_prices = adjust_prices_for_macro_events()  # Adjust stock prices for macro events
    st.line_chart(stock_prices)

    st.write("### PnL Summary")
    total_pnl = sum([trade['price'] * trade['quantity'] for trade in executed_orders])
    st.write(f"Profit and Loss: ${total_pnl}")

    st.write("### Recent Orders")
    st.table(executed_orders)

    st.write("### Macro Events")
    for event in macro_events:
        st.write(f"Upcoming Event: {event['event']} on {event['date']} (Impact: {event['impact']})")

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
    
    if st.button("Place Order"):
        add_order(order_type.lower(), stock, price, quantity)
        st.success("Order placed successfully!")

    st.write("### Order Book")
    st.write("#### Buy Orders")
    st.table(pd.DataFrame(order_book["buy"]))

    st.write("#### Sell Orders")
    st.table(pd.DataFrame(order_book["sell"]))

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
    if st.button("Run"):
        # This should ideally parse and execute the algorithm
        st.write(f"Running algorithm: {code}")
    if st.button("Save"):
        # Save algorithm to a list for future use
        st.write("Algorithm saved.")

    st.write("### Trading Bots")
    bot_count = st.number_input("Number of Bots", 1, 10)
    frequency = st.selectbox("Trading Frequency", ["Every minute", "Hourly", "Daily"])
    
    if st.button("Deploy Bots"):
        for _ in range(bot_count):
            bot_strategies.append({"frequency": frequency})
        st.success(f"{bot_count} bots deployed with {frequency} frequency.")

    st.write(f"Currently running {len(bot_strategies)} bots.")

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
    pnl_data = [trade['price'] * trade['quantity'] for trade in executed_orders]
    st.line_chart({"PnL": pnl_data})

    st.write("### Order History")
    st.table(pd.DataFrame(executed_orders))

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
    
    if st.button("Deploy Bots"):
        for _ in range(bot_count):
            bot_strategies.append({"frequency": frequency})
        st.success(f"{bot_count} bots deployed with {frequency} frequency.")

    execute_bot_trading()  # Simulate bot trading

    st.write("### Bot Performance")
    bot_performance = [{"Bot ID": i+1, "PnL": random.randint(50, 200), "Success Rate": f"{random.randint(70, 90)}%"} for i in range(bot_count)]
    st.table(pd.DataFrame(bot_performance))

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
    for event in macro_events:
        st.write(f"{event['date']}: {event['event']} (Impact: {event['impact']})")

    st.write("### Event Details")
    st.write("Federal Reserve Meeting: Discussion on potential interest rate changes which could affect market volatility.")

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