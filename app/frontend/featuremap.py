import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_DIR = BASE_DIR / "csv"  # locate the prerace folder

pre_race_model = pd.read_csv(MODEL_DIR / "race_model.csv")

