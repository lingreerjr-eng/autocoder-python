import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import yfinance as yf
import warnings
warnings.filterwarnings('ignore')

from data_fetcher import fetch_crypto_data
from model import CryptoPredictor
from signals import generate_signals

def main():
    # Fetch data
    print("Fetching cryptocurrency data...")
    data = fetch_crypto_data('BTC-USD', period='2y')
    
    # Initialize and train model
    print("Training model...")
    predictor = CryptoPredictor()
    predictor.train(data)
    
    # Generate signals
    print("Generating trading signals...")
    signals = generate_signals(predictor, data)
    
    # Display recent signals
    recent_signals = signals.tail(10)
    print("\nRecent Trading Signals:")
    print(recent_signals[['Close', 'Predicted_Price', 'Signal']])
    
    # Current recommendation
    current_signal = signals['Signal'].iloc[-1]
    current_price = data['Close'].iloc[-1]
    print(f"\nCurrent Recommendation: {current_signal}")
    print(f"Current Price: ${current_price:.2f}")

if __name__ == "__main__":
    main()
