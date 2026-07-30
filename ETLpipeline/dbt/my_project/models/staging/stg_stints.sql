-- Store the 'view' of 'stints' table, since it is already existing --

{{config(
    materialized='view'
)}}

select * 
from {{source('dev', 'stints')}}