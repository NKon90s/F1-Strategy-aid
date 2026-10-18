-- Store the 'view' of 'starting_grid' table, since it is already existing --

{{config(
    materialized='view'
)}}

select * 
from {{source('dev', 'starting_grid')}}
