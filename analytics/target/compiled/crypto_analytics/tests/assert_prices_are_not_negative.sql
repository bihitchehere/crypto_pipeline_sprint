select
    coin_id,
    price_usd
from "crypto_database"."main"."stg__prices"
where price_usd < 0