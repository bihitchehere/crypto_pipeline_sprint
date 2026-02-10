import dlt
import requests
from models import CryptoCoin  # Import the rules above

# 1. Define where the data comes from
@dlt.resource(write_disposition="append") # "Append" means add new rows, don't delete old ones
def fetch_coins():
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd..."
    data = requests.get(url).json()

    for coin in data:
        # 2. THE VALIDATION STEP
        # This is where Pydantic checks the data against the rules
        yield CryptoCoin(**coin) 

# 3. The Pipeline Definition
pipeline = dlt.pipeline(
    pipeline_name="crypto_pipeline",
    destination="motherduck",  # Target database
    dataset_name="crypto_raw"  # Target Schema (Folder)
)

# 4. Run it
info = pipeline.run(fetch_coins())