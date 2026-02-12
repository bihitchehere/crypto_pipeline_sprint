select 
    symbol,
    high_24h,
    low_24h
from {{ ref('stg__prices') }}
where high_24h < low_24h   -- ❌ No semicolon here!