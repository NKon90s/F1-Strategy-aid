from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, model_validator, ValidationError, Field
from typing import Annotated, Literal
import uvicorn
from services.predict import predict_compound, predict_stint
import pandas as pd
from services.featuremap import FeatureConfig
from services.simulate_race import SimulateRace
import logging 
import time

# for rate limiting
from fastapi import Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address


####################################################
#
#  This API is for deploying the ML models used
#  for predicting starting compound and first stint
#
####################################################


# Introducing basic logging of requests
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Creating a FastAPI app
app = FastAPI(
    title="F1 Strategy Aid",
    description="Predicts ideal starting compound and first stint length",
    version="1.0.0"
)

# Setting up rate limiter 
limiter = Limiter(key_func=get_remote_address)

app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)


# creating a middleware to log every requests 
@app.middleware("http")
async def log_requests(request, call_next):
    start_time = time.perf_counter()

    try:
        response = await call_next(request)
        duration = time.perf_counter() - start_time

        logger.info(
            "%s %s | Status: %s | Duration: %.3fs",
            request.method,
            request.url.path,
            response.status_code,
            duration
        )
        return response
    
    except Exception:
        logger.exception("Request failed: %s %s", request.method, request.url.path)
        raise


# Defining input schema for Compound prediction using Pydantic
class CompoundInput(BaseModel):
    location: Annotated[str | None, Field(description="The location (city) of the grand prix")]
    avg_track_temperature: Annotated[float | None, Field(description="Average Temperature of the track when race starts")]
    track_length: Annotated[int | None, Field(gt = 0, description="The lengths of the track in meters")]
    n_of_corners: Annotated[int | None, Field(gt = 0,description="How many corners the given track has")]
    degradation: Annotated[Literal['Very-Low','Low','Medium-Low', 'Low-Medium','Medium', 'Medium-High', 'High', 'Very-High'], Field(description="The level of degradation of the given track")]
    overtake_difficulty: Annotated[Literal['Easy', 'Moderate', 'Hard'], Field(description="How difficult it is to perform an overtake")]
    avg_pit_time: Annotated[float | None, Field(gt = 0, description="What is the average pit loss in seconds")]
    driver_number: Annotated[int | None, Field(description="The number of the driver")]
    full_name: Annotated[str | None, Field(description="The full name of the driver")]
    team_name: Annotated[str | None, Field(description="The driver's team")] 
    grid_category: Annotated[Literal['Top-Field', 'Mid-Field', 'Back-Field'], Field(description="Which is the grid category: Top-field, Mid-field, Back-field")]
    dist_hard: Annotated[float | None, Field(ge=0, le=1, description="The distribution of the grid-category using hard compound")]
    dist_medium: Annotated[float | None, Field(ge=0, le=1, description="The distribution of the grid-category using medium compound")]
    dist_soft: Annotated[float | None, Field(ge=0, le=1, description="The distribution of the grid-category using soft compound")]
    driver_baseline_pace: Annotated[float | None, Field(description="The average baseline pace of the given driver by circuit")]
    grid_position: Annotated[int | None, Field(description="The starting grid position of the given driver")]

    @model_validator(mode="after")
    def validate_grid(self):
        if self.grid_position is not None:
            if not 1 <= self.grid_position <= 20:
                raise ValueError("Grid position must be between 1 and 20")
        
        return self

    class Config_Compound:
        schema_extra = {
            "example": {
                "location": "Sakhir",
                "avg_track_temperature": 28.81,
                "track_length": 5412,
                "n_of_corners": 15,
                "degradation": "Very-High",
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
    location: Annotated[str | None, Field(description="The location (city) of the grand prix")]
    avg_track_temperature: Annotated[float | None, Field(description="Average Temperature of the track when race starts")]
    track_length: Annotated[int | None, Field(gt = 0, description="The lengths of the track in meters")]
    n_of_corners: Annotated[int | None, Field(gt = 0, description="How many corners the given track has")]
    degradation: Annotated[Literal['Very-Low','Low','Medium-Low', 'Low-Medium', 'Medium', 'Medium-High', 'High', 'Very-High'], Field(description="The level of degradation of the given track")]
    overtake_difficulty: Annotated[Literal['Easy', 'Moderate', 'Hard'], Field(description="How difficult it is to perform an overtake")]
    tipical_n_of_pitstops: Annotated[int | None, Field(default=1, gt = 0, description="The usual number of pit stops on a given grand prix")]
    avg_pit_time: Annotated[float | None, Field(gt = 0, description="What is the average pit loss in seconds")]
    driver_number: Annotated[int | None, Field(description="The number of the driver")]
    full_name: Annotated[str | None, Field(description="The full name of the driver")]
    team_name: Annotated[str | None, Field(description="The driver's team")] 
    grid_category: Annotated[Literal['Top-Field', 'Mid-Field', 'Back-Field'], Field(description="Which is the grid category: Top-field, Mid-field, Back-field")]
    starting_compound: Annotated[Literal["SOFT", "MEDIUM", "HARD"], Field(description="The starting tyre compound used by the driver")]
    driver_baseline_pace: Annotated[float | None, Field(description="The average baseline pace of the given driver by circuit")]
    grid_position: Annotated[int | None, Field(description="The starting grid position of the given driver")]
    tyre_age_at_start: Annotated[float | None, Field(description="The age of the tyres at start. e.g 0 or 2")]
    avg_hard_stint_by_race: Annotated[float | None, Field(description="The average length of stints performed on a given race on hard")]
    avg_med_stint_by_race: Annotated[float | None, Field(description="The average length of stints performed on a given race on medium")]
    avg_soft_stint_by_race: Annotated[float | None, Field(description="The average length of stints performed on a given race on soft")]
    avg_hard_stint_by_driver: Annotated[float | None, Field(description="The average length of stints performed on a given race by driver on hard")]
    avg_med_stint_by_driver: Annotated[float | None, Field(description="The average length of stints performed on a given race by driver on medium")]
    avg_soft_stint_by_driver: Annotated[float | None, Field(description="The average length of stints performed on a given race by driver on soft")]

    @model_validator(mode="after")
    def validate_grid(self):
        if self.grid_position is not None:
            if not 1 <= self.grid_position <= 20:
                raise ValueError("Grid position must be between 1 and 20")
    
        return self
 
    class Config_Stint:
        schema_extra = {
            "example": {
                "location": "Sakhir",
                "avg_track_temperature": 28.81,
                "track_length": 5412,
                "n_of_corners": 15,
                "degradation": "Very-High",
                "overtake_difficulty": "Hard",
                "tipical_n_of_pitstops": 2,
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


# Defining Response Models with pydantic
class PredictionResponseCompound(BaseModel):
    starting_compound: Literal["SOFT", "MEDIUM", "HARD"]
    prob_hard: float
    prob_med: float
    prob_soft: float

class PredictionResponseStint(BaseModel):
    first_stint_length: float = Field(..., gt=0, le=70)

class CompoundFetchRequest(BaseModel):
    driver: str
    grid_position: int = Field(..., ge=1, le=20)
    asphalt_temperature: float
    selected_gp: str


class StintFetchRequest(BaseModel):
    driver: str
    grid_position: int = Field(..., ge=1, le=20)
    asphalt_temperature: float
    selected_gp: str
    starting_compound: Literal["SOFT", "MEDIUM", "HARD"]
    tyre_age_at_start: int = Field(default=0, ge = 0, le=5)


class SimulateRaceRequest(BaseModel):
    selected_gp: str
    driver: str
    starting_compound: Literal["SOFT", "MEDIUM", "HARD"]
    first_stint: float = Field(..., ge=1)

 

@app.post("/fetch-compound-data")
@limiter.limit("15/minute")  # introducing 10 request per minute rate limit
async def fetch_compound(request: Request, data: CompoundFetchRequest):
    add_features = FeatureConfig(
        data.driver,
        data.grid_position,
        data.asphalt_temperature,
        data.selected_gp
    )

    pred_compound_features = add_features.fetch_compound_params()

    return pred_compound_features


@app.post("/fetch-stint-data")
@limiter.limit("15/minute") # introducing 10 request per minute rate limit
async def fetch_stint(request: Request, data: StintFetchRequest):
    add_features = FeatureConfig(
        data.driver,
        data.grid_position,
        data.asphalt_temperature,
        data.selected_gp
    )
    pred_stint_features = add_features.fetch_stint_params(data.starting_compound)

    return pred_stint_features



@app.post("/predict-compound", response_model=PredictionResponseCompound)
@limiter.limit("15/minute") # introducing 10 request per minute rate limit
async def pred_compound_endpoint(request: Request, data: CompoundInput):
    # model_dump() functiion converts the input into dictionary format
    prediction = predict_compound(data.model_dump())
    
    predicted_tyre  = prediction["prediction"]
    prob_hard = prediction["probabilities"]["HARD"]
    prob_med = prediction["probabilities"]["MEDIUM"]
    prob_soft = prediction["probabilities"]["SOFT"]

    return PredictionResponseCompound(
        starting_compound = predicted_tyre,
        prob_hard = round(prob_hard, 2),
        prob_med = round(prob_med, 2),
        prob_soft = round(prob_soft, 2)
    )


@app.post("/predict-stint", response_model=PredictionResponseStint)
@limiter.limit("15/minute") # introducing 10 request per minute rate limit
async def pred_stint_endpoint(request: Request, data: StintInput):
    # model_dumo() functiion converts the input into dictionary format
    prediction = predict_stint(data.model_dump())
    return PredictionResponseStint(
        first_stint_length = prediction
    )

  
@app.post("/simulate-race")
@limiter.limit("15/minute") # introducing 10 request per minute rate limit
async def simulate_race(request: Request, data: SimulateRaceRequest):
    race_instance = SimulateRace(
        data.selected_gp,
        data.driver,
        data.starting_compound,
        data.first_stint
    )
    race_data = race_instance.fetch_race_data()
    strategy = race_instance.calculate_strategy(race_data)

    return strategy


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
    uvicorn.run(app, host="127.0.0.1", port=9999)