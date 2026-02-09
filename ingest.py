import dlt
import requests
from models import Coin

@dlt.resource(name="raw_prices", write_disposition="replace")
def fetch_coins():
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd"
    data = requests.get(url).json()
    # Validate each item with Pydantic
    yield [Coin(**coin).model_dump() for coin in data]

if __name__ == "__main__":
    pipeline = dlt.pipeline(destination="motherduck", dataset_name="crypto_raw")
    pipeline.run(fetch_coins())