from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, ValidationError, Field
from typing import Annotated
import uvicorn
from predict import predict_compound, predict_stint

####################################################
#
#  This API is for deploying the ML models used
#  for predicting starting compound and first stint
#
####################################################

# Creating a FastAPI app
app = FastAPI(
    title="F1 Strategy Aid",
    description="Predicts ideal starting compound and first stint length",
    version="1.0.0"
)

# Defining input schema for Compound prediction using Pydantic
class CompoundInput(BaseModel):
    location: Annotated[object | None, Field(description="The location (city) of the grand prix")]
    avg_track_temperature: Annotated[float | None, Field(description="Average Temperature of the track when race starts")]
    track_length: Annotated[int | None, Field(description="The lengths of the track in meters")]
    n_of_corners: Annotated[int | None, Field(description="How many corners the given track has")]
    degradation: Annotated[object | None, Field(description="The level of degradation of the given track")]
    overtake_difficulty: Annotated[object | None, Field(description="How difficult it is to perform an overtake")]
    avg_pit_time: Annotated[float | None, Field(description="What is the average pit loss in seconds")]
    driver_number: Annotated[int | None, Field(description="The number of the driver")]
    full_name: Annotated[object | None, Field(description="The full name of the driver")]
    team_name: Annotated[object | None, Field(description="The driver's team")] 
    grid_category: Annotated[object | None, Field(description="Which is the grid category: Top-field, Mid-field, Back-field")]
    dist_hard: Annotated[float | None, Field(description="The distribution of the grid-category using hard compound")]
    dist_medium: Annotated[float | None, Field(description="The distribution of the grid-category using medium compound")]
    dist_soft: Annotated[float | None, Field(description="The distribution of the grid-category using soft compound")]
    driver_baseline_pace: Annotated[float | None, Field(description="The average baseline pace of the given driver by circuit")]
    grid_position: Annotated[int | None, Field(description="The starting grid position of the given driver")]

    class Config:
        schema_extra = {
            "example": {
                "location": "Sakhir",
                "avg_track_temperature": 28.81,
                "track_length": 5412,
                "n_of_corners": 15,
                "degradation": "Very High",
                "overtake_difficulty": "Hard",
                "avg_pit_time": 25.84,
                "driver_number": 1,
                "full_name": "Max VERSTAPPEN",
                "team_name": "Red Bull Racing",
                "grid_category": "Top-Field",
                "dist_hard": 0.06,
                "dist_medium": 0.11,
                "dist_soft": 0.83,
                "driver_baseline_pace": 98.93,
                "grid_position": 1
            }
        }

# Defining input schema for First Stint prediction using Pydantic
class StintInput(BaseModel):
    location: Annotated[object | None, Field(description="The location (city) of the grand prix")]
    avg_track_temperature: Annotated[float | None, Field(description="Average Temperature of the track when race starts")]
    track_length: Annotated[int | None, Field(description="The lengths of the track in meters")]
    n_of_corners: Annotated[int | None, Field(description="How many corners the given track has")]
    degradation: Annotated[object | None, Field(description="The level of degradation of the given track")]
    overtake_difficulty: Annotated[object | None, Field(description="How difficult it is to perform an overtake")]
    avg_pit_time: Annotated[float | None, Field(description="What is the average pit loss in seconds")]
    driver_number: Annotated[int | None, Field(description="The number of the driver")]
    full_name: Annotated[object | None, Field(description="The full name of the driver")]
    team_name: Annotated[object | None, Field(description="The driver's team")] 
    grid_category: Annotated[object | None, Field(description="Which is the grid category: Top-field, Mid-field, Back-field")]
    starting_compound: Annotated[object | None, Field(description="The starting tyre compound used by the driver")]
    driver_baseline_pace: Annotated[float | None, Field(description="The average baseline pace of the given driver by circuit")]
    grid_position: Annotated[int | None, Field(description="The starting grid position of the given driver")]
    tyre_age_at_start: Annotated[float | None, Field(description="The age of the tyres at start. e.g 0 or 2")]
    avg_hard_stint_by_race: Annotated[float | None, Field(description="The average length of stints performed on a given race on hard")]
    avg_med_stint_by_race: Annotated[float | None, Field(description="The average length of stints performed on a given race on medium")]
    avg_soft_stint_by_race: Annotated[float | None, Field(description="The average length of stints performed on a given race on soft")]
    avg_hard_stint_by_driver: Annotated[float | None, Field(description="The average length of stints performed on a given race by driver on hard")]
    avg_med_stint_by_drive: Annotated[float | None, Field(description="The average length of stints performed on a given race by driver on medium")]
    avg_soft_stint_by_driver: Annotated[float | None, Field(description="The average length of stints performed on a given race by driver on soft")]
 
    class Config:
        schema_extra = {
            "example": {
                "location": "Sakhir",
                "avg_track_temperature": 28.81,
                "track_length": 5412,
                "n_of_corners": 15,
                "degradation": "Very High",
                "overtake_difficulty": "Hard",
                "avg_pit_time": 25.84,
                "driver_number": 1,
                "full_name": "Max VERSTAPPEN",
                "team_name": "Red Bull Racing",
                "grid_category": "Top-Field",
                "starting_compound": "HARD",
                "driver_baseline_pace": 98.23,
                "grid_position": 1,
                "tyre_age_at_start": 0.0,
                "avg_hard_stint_by_race": 15.0,
                "avg_med_stint_by_race":13.0,
                "avg_soft_stint_by_race":10.0,
                "avg_hard_stint_by_driver":20.0,
                "avg_med_stint_by_driver":18.0,
                "avg_soft_stint_by_driver:": 14.0
            }
        }

# Defining Response Model with pydantic
class PredictionResponseCompound(BaseModel):
    starting_compound: object

# Defining Response Model with pydantic
class PredictionResponseStint(BaseModel):
    first_stint_length: float



@app.post("/predict-compound", response_model=PredictionResponseCompound)






@app.get("/")
def read_root():
    return {"message": "You are using F1 Strategy Aid API"}


@app.get("/health")
def health_check():
    """Health check endpoint to verify API is running"""
    return {"status": "healthy"}


@app.get("/model-info")
def model_info():
    return {
        "model": "F1 Strategy Aid",
        "version": "1.0",
    }

@app.get("/ping")
def ping():
    return {"message": "API running"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)