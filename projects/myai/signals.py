import pandas as pd
import numpy as np

def generate_signals(predictor, data):
    """Generate buy/sell signals based on model predictions"""
    # Get predictions
    predictions = predictor.predict(data)
    
    # Create signals dataframe
    df = data.copy()
    df = df.iloc[:-1]  # Remove last row since we don't have prediction for it
    df['Predicted_Price'] = predictions[:-1]
    
    # Calculate prediction change
    df['Prediction_Change'] = (df['Predicted_Price'] - df['Close']) / df['Close']
    
    # Generate signals
    # Buy when predicted price is significantly higher (e.g., > 1%)
    # Sell when predicted price is significantly lower (e.g., < -1%)
    # Hold otherwise
    
    conditions = [
        df['Prediction_Change'] > 0.01,  # Buy signal
        df['Prediction_Change'] < -0.01,  # Sell signal
    ]
    
    choices = ['BUY', 'SELL']
    df['Signal'] = np.select(conditions, choices, default='HOLD')
    
    return df
