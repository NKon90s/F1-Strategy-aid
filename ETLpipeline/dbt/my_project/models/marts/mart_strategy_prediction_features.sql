
-- Can be used for 'Should I pit now?' --
{{ config(
    materialized='table'
) }}


WITH laps AS (
    SELECT *
    FROM {{ ref('int_lap_enriched') }}
),

race_context AS (
    SELECT *
    FROM {{ ref('int_race_context') }}
),

race_start AS (
    SELECT *
    FROM {{ ref('int_start_strategy') }}
)

SELECT

l.meeting_key,
l.session_key,
l.driver_number,
l.lap_number,

-- tyre state--
l.compound,
l.tyre_age,

-- pace--
l.avg_previous_5_laps,
l.fuel_corrected_duration,


-- traffic--
l.closest_gap_ahead,

-- weather--
l.avg_track_temperature,
l.rainfall,
avg_air_temperature,
avg_wind_speed,

-- race situation--
r.safety_car,
r.virtual_safety_car,
r.yellow_flag,

-- remaining laps
MAX(l.lap_number)
OVER(
    PARTITION BY l.session_key
)
- l.lap_number
AS laps_remaining,

-- starting conditions
s.grid_position,
s.starting_compound

FROM laps l

LEFT JOIN race_context r
    ON l.session_key=r.session_key
    AND l.lap_number=r.lap_number

LEFT JOIN race_start s
    ON l.session_key=s.session_key
    AND l.driver_number=s.driver_number