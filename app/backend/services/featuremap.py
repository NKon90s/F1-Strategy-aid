import pandas as pd
from pathlib import Path
import numpy as np

BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_DIR = BASE_DIR / "data"  # locate the csv folder

pre_race_model = pd.read_csv(MODEL_DIR / "prerace.csv")

class FeatureConfig:

    def __init__(self, driver, grid_position, asphalt_temperature, selected_gp):
        self.driver = driver
        self.grid_position = grid_position
        self.asphalt_temperature = asphalt_temperature
        self.selected_gp = selected_gp

    def make_json_safe(self, data):
        safe_data = {}

        for key, value in data.items():
            if isinstance(value, np.generic):
                value = value.item()

            if isinstance(value, float) and not np.isfinite(value):
                value = None

            safe_data[key] = value

        return safe_data

    def fetch_compound_params(self):

        gp_data = pre_race_model[pre_race_model['meeting_name'] == self.selected_gp]

        if gp_data.empty:
            raise ValueError(
                f"No data found for Grand Prix: {self.selected_gp}"
            )
 
        driver_data = gp_data[gp_data['full_name'] == self.driver]

        if driver_data.empty:
            raise ValueError(
                f"No data found for {self.driver} at {self.selected_gp}"
            )

        grid_data = gp_data[gp_data['grid_position'] == self.grid_position]

        if grid_data.empty:
            raise ValueError(
                f"No grid position {self.grid_position} found for {self.selected_gp}"
            )


        return self.make_json_safe({
            "location" : gp_data['location'].iloc[0],
            "avg_track_temperature" : self.asphalt_temperature,
            "track_length": gp_data['track_length'].iloc[0],
            "n_of_corners": gp_data['n_of_corners'].iloc[0],
            "degradation": gp_data['degradation'].iloc[0],
            "overtake_difficulty": gp_data['overtake_difficulty'].iloc[0],
            "avg_pit_time": gp_data['avg_pit_time'].iloc[0],
            "driver_number": driver_data['driver_number'].iloc[0],
            "full_name": self.driver,
            "team_name": driver_data['team_name'].iloc[0],
            "grid_category": grid_data['grid_category'].iloc[0],
            "dist_hard": gp_data['dist_hard'].iloc[0],
            "dist_medium": gp_data['dist_medium'].iloc[0],
            "dist_soft": gp_data['dist_soft'].iloc[0],
            "driver_baseline_pace": driver_data['driver_baseline_pace'].iloc[0],
            "grid_position": self.grid_position
        })


    def fetch_stint_params(self, starting_compound, tyre_age_at_start = 0):

        gp_data = pre_race_model[pre_race_model['meeting_name'] == self.selected_gp]

        if gp_data.empty:
            raise ValueError(
                f"No data found for Grand Prix: {self.selected_gp}"
            )

        driver_data = gp_data[gp_data['full_name'] == self.driver] 

        if driver_data.empty:
            raise ValueError(
                f"No data found for {self.driver} at {self.selected_gp}"
            )

        grid_data = gp_data[gp_data['grid_position'] == self.grid_position]

        if grid_data.empty:
            raise ValueError(
                f"No grid position {self.grid_position} found for {self.selected_gp}"
            )

        return self.make_json_safe({
            "location" : gp_data['location'].iloc[0],
            "avg_track_temperature" : self.asphalt_temperature,
            "track_length": gp_data['track_length'].iloc[0],
            "n_of_corners": gp_data['n_of_corners'].iloc[0],
            "degradation": gp_data['degradation'].iloc[0],
            "overtake_difficulty": gp_data['overtake_difficulty'].iloc[0],
            "tipical_n_of_pitstops": gp_data['tipical_n_of_pitstops'].iloc[0],
            "avg_pit_time": gp_data['avg_pit_time'].iloc[0],
            "driver_number": driver_data['driver_number'].iloc[0],
            "full_name": self.driver,
            "team_name": driver_data['team_name'].iloc[0],
            "grid_category": grid_data['grid_category'].iloc[0],
            "starting_compound": starting_compound,
            "driver_baseline_pace": driver_data['driver_baseline_pace'].iloc[0],
            "grid_position": self.grid_position,
            "tyre_age_at_start": tyre_age_at_start,
            "avg_hard_stint_by_race": gp_data['avg_hard_stint_by_race'].iloc[0],
            "avg_med_stint_by_race": gp_data['avg_med_stint_by_race'].iloc[0] ,
            "avg_soft_stint_by_race": gp_data['avg_soft_stint_by_race'].iloc[0],
            "avg_hard_stint_by_driver": driver_data['avg_hard_stint_by_driver'].iloc[0],
            "avg_med_stint_by_driver": driver_data['avg_med_stint_by_driver'].iloc[0],
            "avg_soft_stint_by_driver": driver_data['avg_soft_stint_by_driver'].iloc[0]
        })
    
