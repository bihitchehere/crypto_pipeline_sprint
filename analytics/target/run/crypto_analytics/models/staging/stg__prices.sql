
        
            delete from "crypto_database"."main"."stg__prices"
            where (
                crypto_id_timestamp) in (
                select (crypto_id_timestamp)
                from "crypto_database"."dbt_temp"."stg__prices__8960ef24fb91"
            );

        
    

    insert into "crypto_database"."main"."stg__prices" ("crypto_id_timestamp", "coin_id", "crypto_symbol", "price_usd", "market_cap", "daily_change", "ingested_at")
    (
        select "crypto_id_timestamp", "coin_id", "crypto_symbol", "price_usd", "market_cap", "daily_change", "ingested_at"
        from "crypto_database"."dbt_temp"."stg__prices__8960ef24fb91"
    )
  