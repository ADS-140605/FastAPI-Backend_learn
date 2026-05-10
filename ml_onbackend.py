from fastapi import FastAPI
from joblib import load
import pandas as pd
import uvicorn

app=FastAPI()

# Load trained model
model=load("spotify_model.joblib")

@app.get("/")
def home():
    return {
        "message":"Spotify Streams Prediction API"
    }

@app.post("/predict")
def predict(
    bpm:int,
    danceability:int,
    valence:int,
    energy:int,
    acousticness:int,
    instrumentalness:int,
    liveness:int,
    speechiness:int
):

    data=pd.DataFrame([{
        "bpm":bpm,
        "danceability_%":danceability,
        "valence_%":valence,
        "energy_%":energy,
        "acousticness_%":acousticness,
        "instrumentalness_%":instrumentalness,
        "liveness_%":liveness,
        "speechiness_%":speechiness
    }])

    prediction=model.predict(data)

    return {
        "predicted_streams":float(prediction[0])
    }

if __name__=="__main__":
    uvicorn.run(app,host="127.0.0.1",port=8000)