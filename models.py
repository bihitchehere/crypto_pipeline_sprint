from pydantic import BaseModel, Field
from typing import Optional

# This class name 'Coin' matches what ingest.py is looking for
class Coin(BaseModel):
    id: str
    symbol: str
    name: str
    current_price: float = Field(gt=0) # Ensures price is positive
    market_cap: float
    price_change_percentage_24h: Optional[float] = 0.0