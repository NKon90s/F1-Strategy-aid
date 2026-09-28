import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_DIR = BASE_DIR / "csv"  # locate the csv folder

pre_race_model = pd.read_csv(MODEL_DIR / "race_model.csv")

def fetch_compound_params(driver, grid_position, asphalt_temperature, selected_gp):

    gp_data = pre_race_model[pre_race_model['meeting_name'] == selected_gp]

    if gp_data.empty:
        raise ValueError(
            f"No data found for Grand Prix: {selected_gp}"
        )

    driver_data = gp_data[gp_data['full_name'] == driver]

    if driver_data.empty:
        raise ValueError(
            f"No data found for {driver} at {selected_gp}"
        )

    grid_data = gp_data[gp_data['grid_position'] == grid_position]

    if grid_data.empty:
        raise ValueError(
            f"No grid position {grid_position} found for {selected_gp}"
        )

    driver_baseline_pace = pre_race_model.loc[(pre_race_model['meeting_name'] == selected_gp) & (pre_race_model['full_name'] == driver), 'driver_baseline_pace'].iloc[0]

    return {
        "location" : gp_data['location'].iloc[0],
        "avg_track_temperature" : asphalt_temperature,
        "track_length": gp_data['track_length'].iloc[0],
        "n_of_corners": gp_data['n_of_corners'].iloc[0],
        "degradation": gp_data['degradation'].iloc[0],
        "overtake_difficulty": gp_data['overtake_difficulty'].iloc[0],
        "avg_pit_time": gp_data['avg_pit_time'].iloc[0],
        "driver_number": driver_data['driver_number'].iloc[0],
        "full_name": driver,
        "team_name": driver_data['team_name'].iloc[0],
        "grid_category": grid_data['grid_category'].iloc[0],
        "dist_hard": gp_data['dist_hard'].iloc[0],
        "dist_medium": gp_data['dist_medium'].iloc[0],
        "dist_soft": gp_data['dist_soft'].iloc[0],
        "driver_baseline_pace": driver_baseline_pace,
        "grid_position": grid_position
    }


def fetch_stint_params(driver, grid_position, asphalt_temperature, selected_gp, starting_compound, tyre_age_at_start):

    gp_data = pre_race_model[pre_race_model['meeting_name'] == selected_gp]

    if gp_data.empty:
        raise ValueError(
            f"No data found for Grand Prix: {selected_gp}"
        )

    driver_data = gp_data[gp_data['full_name'] == driver]

    if driver_data.empty:
        raise ValueError(
            f"No data found for {driver} at {selected_gp}"
        )

    grid_data = gp_data[gp_data['grid_position'] == grid_position]

    if grid_data.empty:
        raise ValueError(
            f"No grid position {grid_position} found for {selected_gp}"
        )


    driver_baseline_pace = pre_race_model.loc[(pre_race_model['meeting_name'] == selected_gp) & (pre_race_model['full_name'] == driver), 'driver_baseline_pace'].iloc[0]
    avg_hard_stint_by_driver = pre_race_model.loc[(pre_race_model['meeting_name'] == selected_gp) & 
                                                  (pre_race_model['full_name'] == driver), 'avg_hard_stint_by_driver'].iloc[0]

    avg_med_stint_by_driver = pre_race_model.loc[(pre_race_model['meeting_name'] == selected_gp) & 
                                                      (pre_race_model['full_name'] == driver), 'avg_med_stint_by_driver'].iloc[0]

    avg_soft_stint_by_driver = pre_race_model.loc[(pre_race_model['meeting_name'] == selected_gp) & 
                                                      (pre_race_model['full_name'] == driver), 'avg_soft_stint_by_driver'].iloc[0]

    return {
        "location" : gp_data['location'].iloc[0],
        "avg_track_temperature" : asphalt_temperature,
        "track_length": gp_data['track_length'].iloc[0],
        "n_of_corners": gp_data['n_of_corners'].iloc[0],
        "degradation": gp_data['degradation'].iloc[0],
        "overtake_difficulty": gp_data['overtake_difficulty'].iloc[0],
        "avg_pit_time": gp_data['avg_pit_time'].iloc[0],
        "driver_number": driver_data['driver_number'].iloc[0],
        "full_name": driver,
        "team_name": driver_data['team_name'].iloc[0],
        "grid_category": grid_data['grid_category'].iloc[0],
        "starting_compound": starting_compound,
        "driver_baseline_pace": driver_baseline_pace,
        "grid_position": grid_position,
        "tyre_age_at_start": tyre_age_at_start,
        "avg_hard_stint_by_race": gp_data['avg_hard_stint_by_race'].iloc[0],
        "avg_med_stint_by_race": gp_data['avg_med_stint_by_race'].iloc[0] ,
        "avg_soft_stint_by_race": gp_data['avg_soft_stint_by_race'].iloc[0],
        "avg_hard_stint_by_driver": avg_hard_stint_by_driver,
        "avg_med_stint_by_driver": avg_med_stint_by_driver,
        "avg_soft_stint_by_driver":avg_soft_stint_by_driver
    }

 

features_Stint = [
    "location",
    "avg_track_temperature",
    "track_length",
    "n_of_corners",
    "degradation",
    "overtake_difficulty",
    "tipical_n_of_pitstops",
    "avg_pit_time",
    "driver_number",
    "full_name",
    "team_name",
    "grid_category",
    "starting_compound",
    "driver_baseline_pace",
    "grid_position",
    "tyre_age_at_start",
    "avg_hard_stint_by_race",
    "avg_med_stint_by_race" ,
    "avg_soft_stint_by_race",
    "avg_hard_stint_by_driver",
    "avg_med_stint_by_driver",
    "avg_soft_stint_by_driver"
]