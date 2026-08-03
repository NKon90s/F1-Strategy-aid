{{ config(
    materialized='table'
    )}}

WITH laps AS (

    SELECT

        session_key,
        meeting_key,
        lap_number,
        MIN(lap_start_time) AS lap_start,
        MAX(lap_end_time) AS lap_end

    FROM {{ ref('int_lap_enriched') }}

    GROUP BY
        session_key,
        meeting_key,
        lap_number

),

race_events AS (

    SELECT

        l.session_key,
        l.lap_number,

        MAX(CASE WHEN rc.flag = 'YELLOW' THEN 1 ELSE 0 END) AS yellow_flag,

        MAX(CASE WHEN rc.flag = 'SAFETY CAR' THEN 1 ELSE 0 END) AS safety_car,

        MAX(CASE WHEN rc.flag = 'VSC' THEN 1 ELSE 0 END) AS virtual_safety_car,

        MAX(CASE WHEN rc.flag = 'RED' THEN 1 ELSE 0 END) AS red_flag

    FROM laps l

    LEFT JOIN {{ ref('stg_race_control') }} rc

        ON l.session_key = rc.session_key

        AND rc.date BETWEEN l.lap_start
                        AND l.lap_end

    GROUP BY

        l.session_key,
        l.lap_number
)


SELECT *

FROM race_events