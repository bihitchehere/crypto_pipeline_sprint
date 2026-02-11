
  
    
    

    create  table
      "crypto_database"."main"."coin_trends__dbt_tmp"
  
    as (
      

with source as (
    -- 1. Grab the clean data from staging
    select * from "crypto_database"."main"."stg__prices"
)

select
    coin_id,
    symbol,
    usd_price,
    daily_change,
    ingested_at,
    
    -- 2. BUSINESS LOGIC: Categorize Volatility
    case 
        when daily_change > 5.0  then '🚀 Mooning'
        when daily_change < -5.0 then '💀 Crashing'
        else '😴 Stable'
    end as volatility_flag,

    -- 3. BUSINESS LOGIC: High Risk Flag (Simple Boolean)
    case
        when abs(daily_change) > 10 then true
        else false
    end as is_high_risk

from source
where daily_change is not null -- Safety check!
    );
  
  