with source as (
    select * from {{ source('crypto_source', 'raw_prices') }}
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