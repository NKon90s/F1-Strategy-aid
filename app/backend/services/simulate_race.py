import pandas as pd
from pathlib import Path
 
 
# Identifying the root library parent[1] provides the backend lib
BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_DIR = BASE_DIR / "data"  # locate the models folder

race_model = pd.read_csv(MODEL_DIR / "racemodel.csv")
pre_race_model = pd.read_csv(MODEL_DIR / "prerace.csv")

class SimulateRace:

    TYRE_LIFE = { "SOFT": 120000, "MEDIUM": 220000, "HARD": 330000, }
    COMPOUNDS = ["SOFT", "MEDIUM", "HARD"]
    MIN_STINT = 10

    def __init__(self, selected_gp, driver, starting_compound, first_stint):
        self.selected_gp = selected_gp
        self.driver = driver
        self.starting_compound = starting_compound
        self.first_stint = first_stint
 
    def fetch_race_data(self):

        gp_data = race_model[race_model['meeting_name'] == self.selected_gp]
        
        if gp_data.empty:
            raise ValueError(
                f"No data found for Grand Prix: {self.selected_gp}"
                )
        
        driver_data = gp_data[gp_data['full_name'] == self.driver] 
        
        if driver_data.empty:
            raise ValueError(
                f"No data found for {self.driver} at {self.selected_gp}"
                )
        

        # HARD, MEDIUM and SOFT avg degradation with handling if a compound is missing
        hard_deg = gp_data.loc[gp_data['compound'] == 'HARD', 'Avg_Deg_Rate'].iloc[0] if (gp_data['compound'] == 'HARD').any() else None
        med_deg = gp_data.loc[gp_data['compound'] == 'MEDIUM', 'Avg_Deg_Rate'].iloc[0] if (gp_data['compound'] == 'MEDIUM').any() else None
        soft_deg = gp_data.loc[gp_data['compound'] == 'SOFT', 'Avg_Deg_Rate'].iloc[0] if (gp_data['compound'] == 'SOFT').any() else None

        # A driver's avg pace on certain compounds
        hard_pace = driver_data.loc[driver_data['compound'] == 'HARD', 'driver_pace_by_comp'].iloc[0] if(driver_data['compound'] == 'HARD').any() else None
        med_pace = driver_data.loc[driver_data['compound'] == 'MEDIUM', 'driver_pace_by_comp'].iloc[0] if(driver_data['compound'] == 'MEDIUM').any() else None
        soft_pace = driver_data.loc[driver_data['compound'] == 'SOFT', 'driver_pace_by_comp'].iloc[0] if(driver_data['compound'] == 'SOFT').any() else None

        # Tipical number of pit-stops
        num_of_pitstops = pre_race_model.loc[pre_race_model['meeting_name'] == self.selected_gp, 'tipical_n_of_pitstops'].iloc[0]
        track_length = pre_race_model.loc[pre_race_model['meeting_name'] == self.selected_gp, 'track_length'].iloc[0]

        result = {
            "starting_compound": self.starting_compound,
            "first_stint": self.first_stint,
            "race_laps": gp_data["race_length_laps"].iloc[0],
            "pit_loss": gp_data['avg_pit_time'].iloc[0],
            "hard_deg": hard_deg,
            "medium_deg": med_deg,
            "soft_deg": soft_deg,
            "hard_pace": hard_pace,
            "medium_pace": med_pace,
            "soft_pace": soft_pace,
            "n_pitstops": num_of_pitstops,
            "track_length": track_length
        }

        # This snipet is to prevent numpy return values as they are not compatible with FastAPI json extension.
        # so it will turn np.int64(57) to 57 for example.
        return {
            key: (
                value.item()
                if hasattr(value, "item")
                else value
            )
            for key, value in result.items()
        }


    def calc_stint_time(self, laps: int, compound: str, data: dict) -> float | None:  
        pace = data[f"{compound.lower()}_pace"]
        deg = data[f"{compound.lower()}_deg"]

        # handling missing pace or deg data
        if pace is None or pd.isna(pace): 
            return None

        if deg is None or pd.isna(deg): 
            return None

        return (laps * pace + deg * laps * (laps-1)/2)


    def tyre_life_allows(self, compound : str, laps: int, data: dict) -> bool:
        distance = laps * data["track_length"]
        return distance <= self.TYRE_LIFE[compound]


    # Calculating one stop strategy
    def one_stop_strategy(self, data: dict):
        
        starting_compound = data['starting_compound']
        first_stint = int(data['first_stint'])
        remaining_laps = data['race_laps'] - first_stint
        pit_loss = data['pit_loss']

        if pit_loss is None or pd.isna(pit_loss):
            raise ValueError("Pit-loss data is missing.")

        first_time = self.calc_stint_time(first_stint, starting_compound, data)

        # The starting compound must have valid pace and degradation data.
        if first_time is None:
            raise ValueError(
                f"Missing pace or degradation data for starting compound "
                f"{starting_compound}."
            )
        
        strategies = []

        # Try every possible second compound but not the starting compound
        for second_compound in self.COMPOUNDS:

            # drivers must use at least two compounds
            if second_compound == starting_compound:
                continue

            # Check if the second tyre can physically complete the remaining race
            if not self.tyre_life_allows(second_compound, remaining_laps, data):
                continue

             
            second_time = self.calc_stint_time(remaining_laps, second_compound, data)

            # Skip compounds with missing pace/degradation data. 
            if second_time is None: 
                continue

            total_time = first_time + second_time + pit_loss

            strategies.append({ 
                "starting_compound": starting_compound, 
                "first_stint": first_stint, 
                "second_compound": second_compound, 
                "second_stint": remaining_laps, 
                "pit_lap": first_stint, 
                "race_time": round(total_time, 2) 
                })
            
        if not strategies: 
            raise ValueError( "No feasible one-stop strategies found." )
            
        
        # return strategy with the most optimal time
        return min(
            strategies, key = lambda x: x["race_time"]
            )


    def two_stop_strategy(self, data):
        starting_compound = data['starting_compound']
        first_stint = int(data['first_stint'])
        remaining_laps = data['race_laps'] - first_stint
        pit_loss = data['pit_loss']

        strategies = []

        first_time = self.calc_stint_time(first_stint, starting_compound, data)
        if first_time is None: 
            return None

        for second_compound in self.COMPOUNDS:
            for third_compound in self.COMPOUNDS: 
                # to ensure that at least two different compounds are used
                if len({starting_compound, second_compound, third_compound}) < 2:
                    continue
                for second_stint in range(self.MIN_STINT, remaining_laps - self.MIN_STINT + 1):

                    third_stint = remaining_laps - second_stint
                    # Check if the second tyre can physically complete the remaining race
                    if not self.tyre_life_allows(second_compound, second_stint, data):
                        continue

                    # Check if the second tyre can physically complete the remaining race
                    if not self.tyre_life_allows(third_compound, third_stint, data):
                        continue

                    second_time = self.calc_stint_time(second_stint, second_compound, data)

                    # Missing data -> skip this strategy. 
                    if second_time is None: 
                        continue

                    third_time = self.calc_stint_time(third_stint, third_compound, data)
                
                    # Missing data -> skip this strategy. 
                    if third_time is None: 
                        continue

                    total_time = (first_time + second_time + third_time + 2 * pit_loss)

                    # append every calculated strategy to the pit2_strategies
                    strategies.append({
                            "starting_compound": starting_compound,
                            "first_stint": first_stint,
                            "second_compound": second_compound,
                            "second_stint": second_stint,
                            "third_compound": third_compound,
                            "third_stint": third_stint,
                            "pit1_lap": first_stint,
                            "pit2_lap": first_stint + second_stint,
                            "race_time": round(total_time, 2)
                        })

        if not strategies:
            raise ValueError(
                "No feasible two-stop strategies found. "
                "Check tyre pace, degradation, stint lengths, and tyre-life data."
            )

        # return strategy with the most optimal time
        return min(
            strategies, key = lambda x: x["race_time"]
        )

    # A function to handle if there is no 
    def safe_strategy(self, strategy_func, data):
        try:
            return strategy_func(data)
        except ValueError:
            return {"race_time":99999}

    def calculate_strategy(self, data: dict):
        starting_compound = data['starting_compound']
        first_stint = int(data['first_stint'])
        n_pitstops = int(data['n_pitstops'])

        # Some basic error handling
        if starting_compound not in self.COMPOUNDS:
            raise ValueError(f"Invalid starting compound: {starting_compound}")

        if first_stint <= 0:
            raise ValueError("First stint must be greater than zero.")

        if first_stint >= data['race_laps']:
            raise ValueError("First stint cannot be greater than or equal to the race length.")

        # Calculating the strategy based on different scenarios
        if n_pitstops == 1:
            return {
                "recommended_strategy": self.safe_strategy(self.one_stop_strategy,data),
                "alternative_strategy": self.safe_strategy(self.two_stop_strategy,data)    
            }
 
        elif n_pitstops == 2:
            return {
                "recommended_strategy": self.safe_strategy(self.two_stop_strategy,data),
                "alternative_strategy": self.safe_strategy(self.one_stop_strategy,data)   
            }

        else:
            raise NotImplementedError(f"{n_pitstops} strategies are not implemented yet..")

