select
    coin_id,
    price_usd
from {{ ref('stg__prices') }}
where price_usd < 0