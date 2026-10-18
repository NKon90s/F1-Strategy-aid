# F1 Strategy Aid 
  
This project aims to serve as an aid for F1 tyre strategy decisions. It helps to determine the initial tyre and pit stop strategy via machine learning tools and race simulation techniques. The base data is fetched from [OpenF1 Api](https://openf1.org/). 



 
## Table of contents 

## Requirements 

For specific requirements and dependencies, please read the `requirements.txt` file.
Use for example `pip install` method. E.g:  `pip install -r requirements.txt`

But the docker containers handle the dependencies automatically.

## ELT Pipeline

Training data is ingested through an ELT pipeline. Data is extracted from the `OpenF1 API` using Python’s `requests library` and loaded into a `PostgreSQL database`. Data cleaning, basic data engineering, and transformations are performed using `dbt`. The entire workflow is orchestrated with `Apache Airflow` and containerized using `Docker`.

The schema of the pipeline:

![ELT pipeline](imgs/ETLpipeline.png)

**The following databases have been created via the ELT pipeline:**

These databases have been used to create the training data

- **staging**:
    - stg_car_data
    - stg_drivers
    - stg_intervals
    - stg_laps
    - stg_meetings
    - stg_pit
    - stg_position
    - stg_race_control
    - stg_sesssions
    - stg_starting_grid
    - stg_stints
    - stg_weather
- **intermediate**:
    - int_lap_enriched
    - int_race_context
    - int_start_strategy
    - int_tyre_degradation
- **marts**:
    - mart_start_strategy_features
    - mart_strategy_prediction_features
    - mart_tyre_prediction_features


