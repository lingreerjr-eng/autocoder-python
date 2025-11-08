import yfinance as yf
import pandas as pd

def fetch_crypto_data(symbol, period='1y', interval='1d'):
    """
    Fetch cryptocurrency data using yfinance
    """
    try:
        data = yf.download(symbol, period=period, interval=interval)
        if data.empty:
            raise ValueError(f"No data found for symbol {symbol}")
        return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        # Return sample data for demonstration
        return generate_sample_data()

def generate_sample_data():
    """
    Generate sample data for demonstration purposes
    """
    dates = pd.date_range('2022-01-01', periods=365, freq='D')
    prices = 40000 + np.cumsum(np.random.randn(365) * 1000)
    high = prices * (1 + np.abs(np.random.randn(365) * 0.02))
    low = prices * (1 - np.abs(np.random.randn(365) * 0.02))
    volume = np.random.randint(1000000000, 5000000000, 365)
    
    data = pd.DataFrame({
        'Open': prices * (1 + np.random.randn(365) * 0.005),
        'High': high,
        'Low': low,
        'Close': prices,
        'Volume': volume
    }, index=dates)
    
    return data
