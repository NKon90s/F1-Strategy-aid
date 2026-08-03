
-- It contains data that can be used for 'What will my pace will be in the next n lap ?'--

{{ config(
    materialized='table'
) }}

WITH base AS (
    SELECT *
    FROM {{ ref('int_tyre_degradation') }}
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

        ) AS next_5_lap_average

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
    b.fuel_corrected_duration,
    b.previous_lap_time,
    b.avg_previous_5_laps,

     -- Degradation features--
    b.lap_to_lap_degradation,
    b.rolling_avg_lap,
    b.degradation_from_best,
    b.rolling_degradation,

    -- traffic--
    b.closest_gap_ahead,
    b.is_clean_lap,

    -- weather--
    b.avg_air_temperature,
    b.avg_track_temperature,
    b.avg_humidity,
    b.rainfall,

    -- target--
    t.next_5_lap_average,
    f.best_next_5_lap

FROM base b
LEFT JOIN targets t
    ON b.session_key=t.session_key
    AND b.driver_number=t.driver_number
    AND b.lap_number=t.lap_number
