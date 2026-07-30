-- Store the 'view' of 'weather' table, since it is already existing --

{{config(
    materialized='view'
)}}

select * 
from {{source('dev', 'weather')}}