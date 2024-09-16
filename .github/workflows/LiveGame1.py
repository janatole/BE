import streamlit as st
import pandas as pd
import alpaca_trade_api as tradeapi
import hashlib

# Configuration
ALPACA_API_KEY = 'your_alpaca_api_key'
ALPACA_API_SECRET = 'your_alpaca_api_secret'
ALPACA_BASE_URL = 'https://paper-api.alpaca.markets'  # Use 'https://api.alpaca.markets' for live trading

# Volatile storage for session and player information
sessions = {}
players = {}

# Initialize Alpaca API
api = tradeapi.REST(ALPACA_API_KEY, ALPACA_API_SECRET, ALPACA_BASE_URL, api_version='v2')

def fetch_player_data(api_key):
    # Alpaca don't need to use the api_key here qs it's used for authentication.

    try:
        account = api.get_account()
        positions = api.list_positions()
        
        trades = []
        holdings = {}
        pnl = 0
        
        for position in positions:
            trades.append({
                "stock": position.symbol,
                "quantity": position.qty,
                "price": position.avg_entry_price
            })
            holdings[position.symbol] = position.qty
        
        # Possible PnL calculation (subject to change)
        for position in positions:
            pnl += (position.current_price - position.avg_entry_price) * position.qty
        
        return {
            "trades": trades,
            "holdings": holdings,
            "pnl": pnl
        }
    
    except Exception as e:
        st.error(f"Error fetching player data: {e}")
        return {"trades": [], "holdings": {}, "pnl": 0}

def calculate_rankings(players):
    # Calculate rankings based on PnL
    rankings = []
    for player_hash, player_data in players.items():
        rankings.append({"Player": player_hash, "PnL": player_data.get('pnl', 0)})
    return sorted(rankings, key=lambda x: x["PnL"], reverse=True)

def add_player_to_session(session_id, api_key):
    player_data = fetch_player_data(api_key)
    player_hash = hashlib.md5(api_key.encode()).hexdigest()  # Hash API key for security
    players[player_hash] = player_data
    if session_id in sessions:
        sessions[session_id]["players"].append(player_hash)
    else:
        st.error("Session ID does not exist.")

def main():
    st.title("Trading Game Live")

    st.sidebar.header("Navigation")
    page = st.sidebar.selectbox("Choose a page", ["Home", "Player Rankings", "View Trades", "Holdings", "Manage Sessions"])

    if page == "Home":
        st.header("Welcome to Trading Game Live!")
        st.write("Submit your API key to start tracking your trades.")
        
        api_key = st.text_input("Enter your Alpaca API Key", type="password")
        session_id = st.text_input("Enter Session ID")
        
        if st.button("Join Session"):
            if session_id in sessions:
                add_player_to_session(session_id, api_key)
                st.success(f"Joined session {session_id} successfully!")
            else:
                st.error("Invalid session ID.")
    
    elif page == "Player Rankings":
        st.header("Player Rankings")
        
        session_id = st.selectbox("Select Session", list(sessions.keys()))
        if session_id:
            rankings = calculate_rankings({ph: players[ph] for ph in sessions[session_id]["players"]})
            st.write(pd.DataFrame(rankings, columns=["Player", "PnL"]))
    
    elif page == "View Trades":
        st.header("View Trades")
        
        session_id = st.selectbox("Select Session", list(sessions.keys()))
        if session_id:
            player_id = st.selectbox("Select Player", sessions[session_id]["players"])
            trades = players[player_id]["trades"]
            st.write(pd.DataFrame(trades))
    
    elif page == "Holdings":
        st.header("Current Holdings")
        
        session_id = st.selectbox("Select Session", list(sessions.keys()))
        if session_id:
            player_id = st.selectbox("Select Player", sessions[session_id]["players"])
            holdings = players[player_id]["holdings"]
            st.write(pd.DataFrame(list(holdings.items()), columns=["Stock", "Quantity"]))
    
    elif page == "Manage Sessions":
        st.header("Manage Sessions")
        
        new_session_id = st.text_input("Create a New Session ID")
        if st.button("Create Session"):
            if new_session_id not in sessions:
                sessions[new_session_id] = {"players": []}
                st.success(f"Session {new_session_id} created successfully!")
            else:
                st.error("Session ID already exists.")

if __name__ == "__main__":
    main()
