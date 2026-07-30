
-- Store the 'view' of 'sessions' table, since it is already existing --

{{config(
    materialized='view'
)}}

select * 
from {{source('dev', 'sessions')}}
