 {{ config(
    materialized='table'
    ) }}

WITH base AS (

    SELECT *

    FROM {{ ref('int_lap_enriched') }}

)

SELECT

    meeting_key,
    session_key,
    driver_number,

    stint_number,
    compound,

    lap_number,
    tyre_age,

    lap_duration,

    fuel_corrected_duration,

    closest_gap_ahead,

    is_clean_lap,

    ROW_NUMBER() OVER (

        PARTITION BY
            session_key,
            driver_number,
            stint_number

        ORDER BY lap_number

    ) AS lap_in_stint,

    LAG(fuel_corrected_duration) OVER (

        PARTITION BY
            session_key,
            driver_number,
            stint_number

        ORDER BY lap_number

    ) AS previous_lap_time,

    fuel_corrected_duration
    -

    LAG(fuel_corrected_duration) OVER (

        PARTITION BY
            session_key,
            driver_number,
            stint_number

        ORDER BY lap_number

    ) AS lap_to_lap_degradation,

    AVG(fuel_corrected_duration) OVER (

        PARTITION BY
            session_key,
            driver_number,
            stint_number

        ORDER BY lap_number

        ROWS BETWEEN 2 PRECEDING
        AND CURRENT ROW

    ) AS rolling_avg_lap,

    MIN(fuel_corrected_duration) OVER (

        PARTITION BY
            session_key,
            driver_number,
            stint_number

    ) AS best_lap_in_stint,

    fuel_corrected_duration

    -

    MIN(fuel_corrected_duration) OVER (

        PARTITION BY
            session_key,
            driver_number,
            stint_number

    ) AS degradation_from_best

FROM base