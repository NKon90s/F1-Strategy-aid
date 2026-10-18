{{ config(
    materialized='table'
) }}

SELECT

    s.meeting_key,
    s.session_key,
    s.driver_number,

    -- grid
    s.grid_position,

    CASE
        WHEN s.grid_position < 3
        THEN TRUE
        ELSE FALSE
    END AS front_row,

    CASE
        WHEN s.grid_position <= 10
        THEN TRUE
        ELSE FALSE
    END AS top10,

    -- starting tyre
    s.starting_compound,
    s.tyre_age_at_start,

    -- actual first stint
    s.first_stint_length,

    -- race info
    m.year,
    m.meeting_name,
    m.country_name,
    m.location


FROM {{ ref('int_start_strategy') }} s
    LEFT JOIN {{ ref('stg_meetings') }} m
    ON s.meeting_key=m.meeting_key