
  
  create view "crypto_database"."main"."stg__prices__dbt_tmp" as (
    select
    id as coin_id,
    symbol,
    current_price as usd_price,
    price_change_percentage_24h as daily_change,
    
    now() as ingested_at 
from "crypto_database"."crypto_raw"."raw_prices"
  );
