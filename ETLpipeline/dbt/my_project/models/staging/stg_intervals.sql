-- Store the 'view' of 'intervals' table, since it is already existing --

{{config(
    materialized='view'
)}}

select * 
from {{source('dev', 'interval_data')}}