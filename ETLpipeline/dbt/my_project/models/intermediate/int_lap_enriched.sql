{{config(
    materialized='table'
)}}
 
WITH lap_stints AS (
    SELECT 
        l.meeting_key
        l.session_key,
        l.driver_number,
        l.lap_number,
        l.lap_duration,

        l.date_start AS lap_start_time,
        l.date_start + (l.lap_duration * INTERVAL '1 second') AS lap_end_time,

        s.stint_number,
        s.tyre_age_at_start,
        s.compound,
        s.lap_start,
        s.lap_end,

        --Calculate the tyre age at a given lap --
        l.lap_number - s.lap_start + 1 AS tyre_age

    FROM {{ref('stg_laps')}} l 
    INNER JOIN {{ref('stg_stints')}} s 
        ON l.session_key = s.session_key
        AND l.driver_number = s.driver_number
        -- Assigns the lap to the correct stint window
        AND l.lap_number BETWEEN s.lap_start AND s.lap_end
    WHERE l.lap_duration IS NOT NULL
),


traffic AS (
    SELECT 
        l.session_key,
        l.driver_number,
        l.lap_number,
        -- Use the official OpenF1 column name 'interval' for the gap to the car ahead
        MIN(i.interval) AS closest_gap_ahead
    FROM lap_stints l
    INNER JOIN {{ ref('stg_intervals') }} i
        ON l.session_key = i.session_key
        AND l.driver_number = i.driver_number
        -- Correlate the interval ping to the specific lap window using time
        AND i.date BETWEEN l.lap_start_time AND l.lap_end_time
    GROUP BY 1, 2, 3
)


SELECT
    l.*,
    t.closest_gap_ahead,
    CASE
        WHEN l.tyre_age = 1 THEN FALSE
        WHEN t.closest_gap_ahead IS NULL THEN TRUE
        WHEN t.closes_gap_ahead > 1.5 THEN TRUE
        ELSE FALSE

    END AS is_clean_lap,

    -- Fuel correction assumption:
    -- lap gets ~0.06 sec faster per completed lap due to fuel burn
    l.lap_duration + (l.lap_number * 0.06)
        AS fuel_corrected_duration

FROM lap_stints l 
LEFT JOIN traffic t 
    ON l.session_key = t.session_key
   AND l.driver_number = t.driver_number
   AND l.lap_number = t.lap_number

