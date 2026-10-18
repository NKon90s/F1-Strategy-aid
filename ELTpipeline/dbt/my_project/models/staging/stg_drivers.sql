-- Store the 'view' of 'drivers' table, since it is already existing --

{{config(
    materialized='view'
)}}

select * 
from {{source('dev', 'drivers')}}

