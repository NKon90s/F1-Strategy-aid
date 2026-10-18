
-- Store the 'view' of 'meetings' table, since it is already existing --

{{config(
    materialized='view'
)}}

select * 
from {{source('dev', 'meetings')}}

