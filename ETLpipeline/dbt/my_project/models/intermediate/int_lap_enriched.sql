{{config(
    materialized='table'
)}}
 
WITH lap_stints AS (
    SELECT 
        l.meeting_key,
        l.session_key,
        l.driver_number,
        l.lap_number,
        l.lap_duration,

        l.date_start AS lap_start_time,
        l.date_start + (l.lap_duration * INTERVAL '1 second') AS lap_end_time,

        s.stint_number,
        s.compound,
        s.tyre_age_at_start,
        s.lap_start,
        s.lap_end,

        --Calculate the tyre age at a given lap --
        s.tyre_age_at_start + (l.lap_number - s.lap_start) AS tyre_age

    FROM {{ ref('stg_laps') }} l 
    INNER JOIN {{ ref('stg_stints') }} s 
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
        MIN(i.interval_seconds) AS closest_gap_ahead
    FROM lap_stints l
    INNER JOIN {{ ref('stg_intervals') }} i
        ON l.session_key = i.session_key
        AND l.driver_number = i.driver_number
        -- Correlate the interval ping to the specific lap window using time
        AND i.date BETWEEN l.lap_start_time AND l.lap_end_time
    GROUP BY
        l.session_key,
        l.driver_number,
        l.lap_number
),


weather AS (
    SELECT 
        l.session_key,
        l.lap_number,

        AVG(w.air_temperature) AS avg_air_temperature,
        AVG(w.track_temperature) AS avg_track_temperature,
        AVG(w.humidity) AS avg_humidity,
        AVG(w.pressure) AS avg_pressure,
        MAX(w.rainfall) AS rainfall,
        AVG(w.wind_speed) AS avg_wind_speed,
        AVG(w.wind_direction) AS avg_wind_direction

    FROM lap_stints l

    LEFT JOIN {{ ref('stg_weather') }} w

         ON l.session_key = w.session_key

        AND w.date BETWEEN
            l.lap_start_time
            AND l.lap_end_time

    GROUP BY

        l.session_key,
        l.lap_number
),

features AS (
    SELECT
        l.*,
        t.closest_gap_ahead,
        w.avg_air_temperature,
        w.avg_track_temperature,
        w.avg_humidity,
        w.avg_pressure,
        w.rainfall,
        w.avg_wind_speed,
        w.avg_wind_direction,

        CASE
            WHEN l.tyre_age = 1 THEN FALSE
            WHEN t.closest_gap_ahead IS NULL THEN TRUE
            WHEN t.closest_gap_ahead > 1.5 THEN TRUE
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

    LEFT JOIN weather w

        ON l.session_key = w.session_key
        AND l.lap_number = w.lap_number

)

SELECT 
    *,

    -- what the model knows before this lap

    LAG(fuel_corrected_duration) OVER(

        PARTITION BY 
            session_key,
            driver_number

        ORDER BY lap_number

    ) AS previous_lap_time,

    LAG(fuel_corrected_duration) OVER(

        PARTITION BY 
            session_key,
            driver_number,
            stint_number

        ORDER BY lap_number

    ) AS previous_stint_lap_time,


    AVG(fuel_corrected_duration) OVER(

        PARTITION BY 
            session_key,
            driver_number

        ORDER BY lap_number

        ROWS BETWEEN 5 PRECEDING 
        AND 1 PRECEDING

    ) AS avg_previous_5_laps,

    AVG(fuel_corrected_duration) OVER(

        PARTITION BY 
            session_key,
            driver_number,
            stint_number

        ORDER BY lap_number

        ROWS BETWEEN 5 PRECEDING 
        AND 1 PRECEDING

    ) AS avg_previous_5_stint_laps


FROM features