import requests
import json
from datetime import datetime

def fetch_prices(coins, currency="usd"):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": ",".join(coins),
        "vs_currencies": currency,
        "include_market_cap": "true",
        "include_24hr_vol": "true",
        "include_24hr_change": "true"
    }
    
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.Timeout:
        print("Error: Request timeout")
        return None
    except requests.exceptions.ConnectionError:
        print("Error: Connection failed")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def format_data(prices):
    formatted = {}
    for coin, values in prices.items():
        change = values.get("usd_24h_change", 0)
        formatted[coin] = {
            "price": values.get("usd"),
            "market_cap": values.get("usd_market_cap"),
            "volume_24h": values.get("usd_24h_vol"),
            "change_24h": change,
            "trend": "up" if change > 0 else "down"
        }
    return formatted

def display_results(data):
    print("\n" + "=" * 50)
    for coin, stats in data.items():
        direction = "+" if stats['change_24h'] > 0 else ""
        print(f"\n{coin.upper()}")
        print(f"  Price: ${stats['price']:,.2f}")
        print(f"  24h Change: {direction}{stats['change_24h']:.2f}%")
        print(f"  Market Cap: ${stats['market_cap']:,.0f}")
        print(f"  Volume 24h: ${stats['volume_24h']:,.0f}")
    print("\n" + "=" * 50)

def save_json(data, filename="crypto_data.json"):
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Error saving file: {e}")

if __name__ == "__main__":
    coins = ["bitcoin", "ethereum", "cardano", "solana"]
    
    print("Crypto Price Tracker")
    prices = fetch_prices(coins)
    
    if prices:
        data = format_data(prices)
        display_results(data)
        save_json(data)
        print(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print("Failed to fetch data")