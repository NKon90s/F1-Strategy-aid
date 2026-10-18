
-- It contains data that can be used for 'What will my pace will be in the next n lap ?'--

{{ config(
    materialized='table'
) }}

WITH base AS (
    SELECT *
    FROM {{ ref('int_tyre_degradation') }}
),

laps AS (
    SELECT *
    FROM {{ ref('int_lap_enriched') }}
),

targets AS (

    SELECT

        session_key,
        driver_number,
        lap_number,
        AVG(fuel_corrected_duration) OVER(

            PARTITION BY
                session_key,
                driver_number

            ORDER BY lap_number

            ROWS BETWEEN 1 FOLLOWING
            AND 5 FOLLOWING

        ) AS next_5_lap_average,

        MIN(fuel_corrected_duration) OVER(

            PARTITION BY
                session_key,
                driver_number

            ORDER BY lap_number

            ROWS BETWEEN 1 FOLLOWING
            AND 5 FOLLOWING

        ) AS best_next_5_lap

    FROM base
)


SELECT

    b.meeting_key,
    b.session_key,
    b.driver_number,
    b.lap_number,

    -- tyre state--
    b.compound,
    b.tyre_age,
    b.stint_number,
    b.best_lap_in_stint,

    -- current pace--
    b.lap_duration,
    b.fuel_corrected_duration,
    b.previous_lap_time,
    b.previous_stint_lap_time,
    b.avg_previous_5_laps,
    b.avg_previous_5_stint_laps,

     -- Degradation features--
    b.lap_to_lap_degradation,
    b.rolling_avg_lap,
    b.degradation_from_best,
    b.rolling_degradation,

    -- traffic--
    b.position_at_lap_end,
    b.gap_to_leader_seconds,
    b.closest_gap_ahead,
    b.is_lapped,
    b.is_clean_lap,

    -- remaining laps
    MAX(l.lap_number)
    OVER(
        PARTITION BY l.session_key
    )
    - l.lap_number
    AS laps_remaining,

    -- weather--
    b.avg_air_temperature,
    b.avg_track_temperature,
    b.avg_humidity,
    b.rainfall,

    -- target--
    t.next_5_lap_average,
    t.best_next_5_lap

FROM base b
LEFT JOIN targets t
    ON b.session_key=t.session_key
    AND b.driver_number=t.driver_number
    AND b.lap_number=t.lap_number

LEFT JOIN laps l
    ON b.session_key=l.session_key
    AND b.driver_number=l.driver_number
    AND b.lap_number=l.lap_number
