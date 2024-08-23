import pandas as pd
import time
import seaborn as sns
import matplotlib.pyplot as plt
from tqdm import tqdm

def set_starting_trading():
    wallet_start = {"usdt": 1000, "coin": 0}
    wallet = wallet_start.copy()

    parameters = {
        "wallet": 1000,
        "usdt": 1000,
        "coin": 0,
        "taker_fee": 0.0007,
        "maker_fee": 0.0002,
        "balance_percentage_usdt": 0.1,
        "balance_percentage_coin": 1,
        "symbol": "BTC/USDT",
        "num_trades": 0,
        "trade_status": "None",
    }
    parameters_records = pd.DataFrame(columns=list(parameters.keys()))

    return wallet_start, wallet, parameters, parameters_records

# Function to calculate wallet value
def calculate_value_wallet(wallet, row):
    return wallet["usdt"] + wallet["coin"] * row["close"]

# Function to execute a trade
def execute_trade(wallet, row, trade_type, parameters):
    if trade_type == "Buy" and wallet["usdt"] > 0:
        # Calculate amount of coin to buy
        amount_coin = (wallet["usdt"] * parameters["balance_percentage_usdt"]) / row["close"]
        wallet["coin"] += amount_coin * (1 - parameters["taker_fee"])
        wallet["usdt"] -= wallet["usdt"] * parameters["balance_percentage_usdt"]
        trade_status = "Buy"
    elif trade_type == "Sell" and wallet["coin"] > 0:
        # Calculate amount of coin to sell
        amount_usdt = wallet["coin"] * row["close"] * parameters["balance_percentage_coin"]
        wallet["usdt"] += amount_usdt * (1 - parameters["taker_fee"])
        wallet["coin"] -= wallet["coin"] * parameters["balance_percentage_coin"]
        trade_status = "Sell"
    else:
        trade_status = "Hold"
    
    return wallet, trade_status

# Simulation loop
def backtesting(data, wallet_start, parameters,strategy):
    wallet_values = []
    parameters_records = pd.DataFrame(columns=list(parameters.keys()))

    for idx, row in tqdm(data.iterrows(), total=len(data), desc="Simulating"):
        current_wallet_value = calculate_value_wallet(wallet_start, row)
        parameters["wallet"] = current_wallet_value
        wallet_values.append(current_wallet_value)

        # Simple trading strategy: buy if price is above MA, sell if below
        if strategy(row) == "buy":
            wallet_start, trade_status = execute_trade(wallet_start, row, "Buy", parameters)
        elif strategy(row) == "sell":
            wallet_start, trade_status = execute_trade(wallet_start, row, "Sell", parameters)
        else:
            trade_status = "Hold"

        # Update parameters and record trade
        parameters["num_trades"] += 1
        parameters["trade_status"] = trade_status
        parameters_records = pd.concat([parameters_records, pd.DataFrame([parameters])], ignore_index=True)

    # Evaluate performance
    final_wallet_value = calculate_value_wallet(wallet_start, data.iloc[-1])
    print(f"Final wallet value: {final_wallet_value}")
    print(f"Number of trades: {parameters['num_trades']}")

    # Plot wallet value over time
    data['wallet_value'] = wallet_values

    return data,wallet_values, parameters_records, final_wallet_value

