{{ config(
    materialized='table'
    )}}

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

    previous_lap_time,

    avg_previous_5_laps,

    fuel_corrected_duration - previous_lap_time AS lap_to_lap_degradation,

   AVG(fuel_corrected_duration) OVER(

        PARTITION BY

            session_key,
            driver_number,
            stint_number

        ORDER BY lap_number

        ROWS BETWEEN 3 PRECEDING 
        AND CURRENT ROW

    )

    AS rolling_avg_lap,


    -- best lap achieved in stint

    MIN(fuel_corrected_duration) OVER(

        PARTITION BY

            session_key,
            driver_number,
            stint_number

    ) AS best_lap_in_stint,

    -- how far tyre is from peak

    lap_duration

    -

    MIN(fuel_corrected_duration) OVER(

        PARTITION BY

            session_key,
            driver_number,
            stint_number

    ) AS degradation_from_best,



    -- degradation trend

    AVG(

        fuel_corrected_duration
        -
        previous_lap_time

    ) OVER(

        PARTITION BY

            session_key,
            driver_number,
            stint_number

        ORDER BY lap_number

        ROWS BETWEEN 3 PRECEDING
        AND CURRENT ROW

    )

    AS rolling_degradation


FROM base


