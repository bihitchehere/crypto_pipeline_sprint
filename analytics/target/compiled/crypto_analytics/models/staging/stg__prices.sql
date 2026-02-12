/*
 old code before incremented it
with source as (
    select * from "crypto_database"."crypto_raw"."raw_prices"
),

renamed as (
    select
        id as coin_id,
        symbol,
        current_price as usd_price,
        market_cap,
        price_change_percentage_24h as daily_change,
        
        -- The fix you made for the timestamp
        now() as ingested_at
    from source
)

select * from renamed

*/



WITH raw_data AS (
    SELECT *
    FROM "crypto_database"."crypto_raw"."raw_prices"
)

SELECT
    -- Use a surrogate key using existing columns
    md5(concat(cast(id as text), '-', cast(symbol as text))) as crypto_id_timestamp,
    id as coin_id,
    symbol as crypto_symbol,
    current_price as price_usd,
    market_cap,
    price_change_percentage_24h as daily_change,
    now() as ingested_at
FROM raw_data


    -- Only process new rows
    WHERE now() > (SELECT MAX(ingested_at) FROM "crypto_database"."main"."stg__prices")
