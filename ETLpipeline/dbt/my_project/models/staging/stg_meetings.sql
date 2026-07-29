{{config(
    materialized='view'
)}}

select * 
from {{source('dev', 'meetings')}}

