select 
    symbol,
    high_24h,
    low_24h
from "crypto_database"."main"."stg__prices"
where high_24h < low_24h   -- ❌ No semicolon here!