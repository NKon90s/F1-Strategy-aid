{{ config(
    materialized='table'
    )}}

WITH first_stint AS (
    SELECT
        meeting_key,
        session_key,
        driver_number,
        compound,
        tyre_age_at_start,
        lap_start,
        lap_end,
        lap_end - lap_start + 1 AS first_stint_length

    FROM {{ ref('stg_stints') }}
    WHERE stint_number = 1
) 

SELECT 
    sg.meeting_key,
    sg.session_key,
    sg.driver_number,
    sg.position AS grid_position,
    fs.compound AS starting_compound,
    fs.tyre_age_at_start,
    fs.first_stint_length,

    CASE
        WHEN sg.position <= 10
        THEN TRUE
        ELSE FALSE
    END AS top10_start,

    CASE
        WHEN sg.position <= 3
        THEN TRUE
        ELSE FALSE
    END AS podium_start

FROM {{ ref('stg_starting_grid') }} sg 

LEFT JOIN first_stint fs 
ON sg.meeting_key = fs.meeting_key
AND sg.driver_number = fs.driver_number

