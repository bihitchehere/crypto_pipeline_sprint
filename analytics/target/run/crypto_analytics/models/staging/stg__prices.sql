
  
  create view "crypto_db"."main"."stg__prices__dbt_tmp" as (
    with source as (
    select * from "crypto_db"."staging"."raw_prices"
),

renamed as (
    select
        id as coin_id,
        symbol,
        name,
        current_price as usd_price,
        market_cap,
        price_change_percentage_24h,
        _dlt_load_id as load_id, -- Keep audit columns!
        current_timestamp as ingested_at
    from source
)

select * from renamed
  );
