with source as (
    -- 1. Grab raw data
    select * from {{ source('crypto_raw', 'raw_prices') }}
),

renamed as (
    select
        -- IDs
        id as coin_id,
        symbol,
        
        -- Prices (These were MISSING before!)
        current_price as usd_price,
        high_24h,       -- <--- Crucial for the test!
        low_24h,        -- <--- Crucial for the test!
        
        -- Metrics
        market_cap,
        price_change_percentage_24h as daily_change,
        
        -- Your Fix: Timestamping ingestion
        now() as ingested_at
    from source
)

select * from renamed