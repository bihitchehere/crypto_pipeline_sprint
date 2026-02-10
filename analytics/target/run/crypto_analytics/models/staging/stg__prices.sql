
  
  create view "crypto_db"."main"."stg__prices__dbt_tmp" as (
    select
    id as coin_id,
    symbol,
    current_price as usd_price,
    price_change_percentage_24h as daily_change,
    updated_at as ingested_at
from "crypto_db"."crypto_raw"."fetch_coins" 
-- referencing the source we defined above
  );
