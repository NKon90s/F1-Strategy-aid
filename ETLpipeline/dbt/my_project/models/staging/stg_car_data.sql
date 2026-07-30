-- Store the 'view' of 'car_data' table, since it is already existing --

{{config(
    materialized='view'
)}}

select * 
from {{source('dev', 'car_data')}}
