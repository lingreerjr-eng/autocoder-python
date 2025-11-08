import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

class CryptoPredictor:
    def __init__(self, n_estimators=100, random_state=42):
        self.model = RandomForestRegressor(n_estimators=n_estimators, random_state=random_state)
        self.feature_columns = []
    
    def create_features(self, data):
        """Create features for the model"""
        df = data.copy()
        
        # Price-based features
        df['Price_Change'] = df['Close'].pct_change()
        df['High_Low_Pct'] = (df['High'] - df['Low']) / df['Close']
        df['Price_Volume_Trend'] = (df['Close'] - df['Open']) / df['Volume']
        
        # Moving averages
        df['MA_5'] = df['Close'].rolling(window=5).mean()
        df['MA_10'] = df['Close'].rolling(window=10).mean()
        df['MA_20'] = df['Close'].rolling(window=20).mean()
        df['MA_50'] = df['Close'].rolling(window=50).mean()
        
        # RSI
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # Volatility
        df['Volatility'] = df['Close'].rolling(window=10).std()
        
        # Lag features
        df['Close_Lag1'] = df['Close'].shift(1)
        df['Close_Lag2'] = df['Close'].shift(2)
        df['Close_Lag3'] = df['Close'].shift(3)
        
        # Target variable (next day's closing price)
        df['Target'] = df['Close'].shift(-1)
        
        # Select feature columns
        self.feature_columns = [col for col in df.columns if col not in ['Target', 'Open', 'High', 'Low', 'Close', 'Volume']]
        
        return df.dropna()
    
    def train(self, data):
        """Train the model"""
        # Create features
        df = self.create_features(data)
        
        # Prepare data
        X = df[self.feature_columns]
        y = df['Target']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train model
        self.model.fit(X_train, y_train)
        
        # Store training data for reference
        self.X_train = X_train
        self.y_train = y_train
        
    def predict(self, data):
        """Make predictions"""
        df = self.create_features(data)
        X = df[self.feature_columns]
        predictions = self.model.predict(X)
        return predictions
