-- Store the 'view' of 'intervals' table, since it is already existing --

{{config(
    materialized='view'
)}}

SELECT 
    id,
    date,
    meeting_key,
    session_key,
    entry_date,
    driver_number,
    gap_to_leader,
    interval AS raw_interval,

    CASE
        WHEN interval LIKE '%LAP%'
        THEN NULL
        ELSE REPLACE(interval, '+', '')::numeric
    END AS interval_seconds


FROM {{source('dev', 'interval_data')}}