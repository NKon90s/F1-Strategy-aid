-- Store the 'view' of 'race_control' table, since it is already existing --

{{config(
    materialized='view'
)}}

select * 
from {{source('dev', 'race_control')}}
