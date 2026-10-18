-- Store the 'view' of 'laps' table, since it is already existing --

{{config(
    materialized='view'
)}}

select * 
from {{source('dev', 'laps')}}