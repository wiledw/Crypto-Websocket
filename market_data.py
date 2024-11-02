import requests
import time
from config import COINGECKO_API_URL, DEFAULT_CURRENCY 
import random

# Function to fetch market data from CoinGecko
def get_market_data(assets):
  """
  Fetch market data for specified assets from the CoinGecko API.

  Parameters:
  assets (dict): A dictionary mapping asset names to their symbols used by the API.

  Returns:
  dict: Market data for the requested assets, with asset symbols as keys. 
        Returns an empty dictionary if there's an error.

  Raises:
  requests.RequestException: Handles errors from the API request.

  Note:
  The function may simulate API downtime for testing (currently commented out).
  """
  
  symbols = ",".join([assets.get(asset.lower(), asset) for asset in assets if asset.lower() in assets])
  # print(symbols)

  # Acts as an side effect (API Down) and return nothing
  # randomNum = random.randrange(0,2)
  # print(randomNum)
  # if randomNum == 1:
  #   print("exiting...")
  #   return {}

  params = {
        'ids': symbols,
        'vs_currencies': DEFAULT_CURRENCY,
        'include_24hr_change': 'true',
        'include_last_updated_at': 'true'
  }
  # print(params)
  try:
    print("Send request to CoinGecko")
    response = requests.get(COINGECKO_API_URL, params=params)
    # print("Raw response:", response.text) 
    response.raise_for_status()
    return response.json()
  except requests.RequestException as e:
    print(f"Error fetching market data: {e}")
    return {}
  
# Function to format market data for WebSocket response
def format_market_data(asset, data):
    # Extract the necessary information from the data
    current_price = data.get(DEFAULT_CURRENCY)
    change_percentage = data.get(f'{DEFAULT_CURRENCY}_24h_change', 0)

    # Ensure current_price is not None before rounding
    if current_price is None:
        # print(f"Warning: Current price for {asset} is None. Data: {data}")
        current_price = 0  # Default to 0 or handle as needed
        change_percentage = 0  # Default to 0 as well if desired

    # Prepare the response data structure
    return {
        "symbol": f"{asset.upper()}_{DEFAULT_CURRENCY.upper()}", 
        "timestamp": int(time.time()), 
        "bid": current_price * 0.995,  # Simulate bid price slightly lower than spot price
        "ask": current_price * 1.005,  # Simulate ask price slightly higher than spot price
        "spot": current_price,         
        "change": round(change_percentage, 2) if change_percentage else 0  # Handle rounding safely
    }


# result = get_market_data(assets=real_assets)
# print(result)