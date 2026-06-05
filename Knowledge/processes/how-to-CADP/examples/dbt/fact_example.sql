-- Example CADP fact model: one row per contract per day
with base as (
  select
    contract_id,
    cast(date as date) as date_key,
    coalesce(revenue, 0) as revenue
  from {{ ref('stg_contracts') }}
)
select
  contract_id,
  date_key,
  sum(revenue) as daily_revenue
from base
where contract_id is not null
  and date_key is not null
group by contract_id, date_key