-- Store the 'view' of 'position' table, since it is already existing --

{{config(
    materialized='view'
)}}

select * 
from {{source('dev', 'position')}}
