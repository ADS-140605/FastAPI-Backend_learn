from fastapi import FastAPI
from pydantic import BaseModel
from joblib import load
import pandas as pd
import uvicorn
from typing import Optional

app = FastAPI()

# Load trained artifacts
artifacts = load("spotify_model.joblib")
model = artifacts["model"]
le_key = artifacts["le_key"]
le_mode = artifacts["le_mode"]
features = artifacts["features"]

# Comprehensive Request schema matching the perfected model
class SongFeatures(BaseModel):
    artist_count: int = 1
    released_year: int = 2023
    released_month: int = 1
    in_spotify_playlists: int = 0
    in_spotify_charts: int = 0
    in_apple_playlists: int = 0
    in_apple_charts: int = 0
    in_deezer_playlists: int = 0
    in_deezer_charts: int = 0
    in_shazam_charts: int = 0
    bpm: int = 120
    key: str = "C#"  # Categorical
    mode: str = "Major"  # Categorical
    danceability: int = 50
    valence: int = 50
    energy: int = 50
    acousticness: int = 50
    instrumentalness: int = 0
    liveness: int = 10
    speechiness: int = 5

@app.get("/")
def home():
    return {
        "message": "Spotify Streams Prediction API (Perfected Model)",
        "features_required": features
    }

@app.post("/predict")
def predict(song: SongFeatures):
    # Prepare input data
    input_data = {
        "artist_count": song.artist_count,
        "released_year": song.released_year,
        "released_month": song.released_month,
        "in_spotify_playlists": song.in_spotify_playlists,
        "in_spotify_charts": song.in_spotify_charts,
        "in_apple_playlists": song.in_apple_playlists,
        "in_apple_charts": song.in_apple_charts,
        "in_deezer_playlists": song.in_deezer_playlists,
        "in_deezer_charts": song.in_deezer_charts,
        "in_shazam_charts": song.in_shazam_charts,
        "bpm": song.bpm,
        "danceability_%": song.danceability,
        "valence_%": song.valence,
        "energy_%": song.energy,
        "acousticness_%": song.acousticness,
        "instrumentalness_%": song.instrumentalness,
        "liveness_%": song.liveness,
        "speechiness_%": song.speechiness,
    }

    # Calculate engineered features
    input_data["total_playlists"] = (
        song.in_spotify_playlists + 
        song.in_apple_playlists + 
        song.in_deezer_playlists
    )

    # Encode categorical features
    # Note: Use try-except or check classes if unknown labels might be sent
    try:
        input_data["key"] = le_key.transform([song.key])[0]
    except:
        input_data["key"] = le_key.transform(["Unknown"])[0]

    try:
        input_data["mode"] = le_mode.transform([song.mode])[0]
    except:
        # Default to most common if unknown
        input_data["mode"] = le_mode.transform(["Major"])[0]

    # Convert to DataFrame in the correct feature order
    df = pd.DataFrame([input_data])[features]

    prediction = model.predict(df)

    return {
        "predicted_streams": int(prediction[0]),
        "status": "success"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
