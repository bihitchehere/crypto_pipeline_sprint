
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  select
    coin_id,
    price_usd
from "crypto_database"."main"."stg__prices"
where price_usd < 0
  
  
      
    ) dbt_internal_test