from pydantic import BaseModel

class CryptoCoin(BaseModel):
    # The Rules:
    id: str                 # Must be text
    symbol: str             # Must be text
    current_price: float    # Must be a number (no "banana")
    market_cap: int         # Must be an integer
    total_volume: int       # Must be an integer
    price_change_percentage_24h: float  # Must be a number (no "banana")