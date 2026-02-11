import dlt
import requests
from models import CryptoCoin
from pydantic import ValidationError

@dlt.resource(table_name="raw_prices", write_disposition="append")
def fetch_coins():
    """
    Fetches coins safely. If one coin is bad, we skip it.
    If the API fails, we print the error instead of crashing.
    """
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 100,
        "page": 1,
        "sparkline": "false"
    }

    try:
        # 1. Try to get data from the API
        print(f"📡 Connecting to {url}...")
        response = requests.get(url, params=params)
        response.raise_for_status() # Check for 404 or 500 errors
        data = response.json()

        # 2. Check if the API sent us a list (valid) or an error dictionary (invalid)
        if not isinstance(data, list):
            print(f"❌ API Error: Expected a list but got: {data}")
            return

    except requests.exceptions.RequestException as e:
        print(f"❌ Network Error: Could not connect to CoinGecko. Reason: {e}")
        return

    # 3. Process each coin one by one
    print(f"✅ API Success! Processing {len(data)} coins...")
    
    for coin in data:
        try:
            # Validate with Pydantic
            yield CryptoCoin(**coin)
        except ValidationError as e:
            # If one coin is bad, just skip it and continue!
            print(f"⚠️ Skipping bad coin data: {coin.get('id', 'Unknown')} - {e}")
        except Exception as e:
            print(f"⚠️ Unexpected error on coin: {e}")

if __name__ == "__main__":
    # Define the pipeline
    pipeline = dlt.pipeline(
        pipeline_name="crypto_pipeline",
        destination="motherduck", 
        dataset_name="crypto_raw"
    )

    # Run it safely
    try:
        print("🚀 Starting pipeline run...")
        load_info = pipeline.run(fetch_coins())
        print(load_info)
        print("🎉 SUCCESS! Data loaded to MotherDuck.")
    except Exception as e:
        print(f"💥 CRITICAL FAILURE: The pipeline crashed. Reason: {e}")