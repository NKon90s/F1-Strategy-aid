-- Store the 'view' of 'pit' table, since it is already existing --

{{config(
    materialized='view'
)}}

select * 
from {{source('dev', 'pit')}}
