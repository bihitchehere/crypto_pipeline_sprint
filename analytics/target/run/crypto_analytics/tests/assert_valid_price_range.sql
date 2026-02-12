
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  select 
    symbol,
    high_24h,
    low_24h
from "crypto_database"."main"."stg__prices"
where high_24h < low_24h   -- ❌ No semicolon here!
  
  
      
    ) dbt_internal_test