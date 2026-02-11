select
    id as coin_id,
    symbol,
    current_price as usd_price,
    price_change_percentage_24h as daily_change,
    
    now() as ingested_at 
from {{ source('crypto_sources', 'raw_prices') }}