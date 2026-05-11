import streamlit as st
import requests
API_URL = "http://127.0.0.1:8000/predict"
st.title("Spotify Streams Prediction")
st.markdown("Enter song features to predict the number of streams.")

# Input fields
artist_count = st.number_input("Artist Count", min_value=1, value=1)
released_year = st.number_input("Released Year", min_value=1900, max_value=2024, value=2023)
released_month = st.number_input("Released Month", min_value=1, max_value=12, value=1)
in_spotify_playlists = st.number_input("In Spotify Playlists", min_value=0, value=0)
in_spotify_charts = st.number_input("In Spotify Charts", min_value=0, value=0)
in_apple_playlists = st.number_input("In Apple Playlists", min_value=0, value=0)
in_apple_charts = st.number_input("In Apple Charts", min_value=0, value=0)
in_deezer_playlists = st.number_input("In Deezer Playlists", min_value=0, value=0)
in_deezer_charts = st.number_input("In Deezer Charts", min_value=0, value=0)
in_shazam_charts = st.number_input("In Shazam Charts", min_value=0, value=0)
bpm = st.number_input("BPM", min_value=0, value=120)    
key = st.selectbox("Key", ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"])
mode = st.selectbox("Mode", ["Major", "Minor"]) 
danceability = st.number_input("Danceability (%)", min_value=0, max_value=100, value=50)
valence = st.number_input("Valence (%)", min_value=0, max_value=100, value=50)
energy = st.number_input("Energy (%)", min_value=0, max_value=100, value=50)
acousticness = st.number_input("Acousticness (%)", min_value=0, max_value=100, value=50)
instrumentalness = st.number_input("Instrumentalness (%)", min_value=0, max_value=100, value=0)
liveness = st.number_input("Liveness (%)", min_value=0, max_value=100, value=10)
speechiness = st.number_input("Speechiness (%)", min_value=0, max_value=100, value=5)   

if st.button("Predict Streams"):
    input_data = {
        "artist_count": int(artist_count),
        "released_year": int(released_year),
        "released_month": int(released_month),
        "in_spotify_playlists": int(in_spotify_playlists),
        "in_spotify_charts": int(in_spotify_charts),
        "in_apple_playlists": int(in_apple_playlists),
        "in_apple_charts": int(in_apple_charts),
        "in_deezer_playlists": int(in_deezer_playlists),
        "in_deezer_charts": int(in_deezer_charts),
        "in_shazam_charts": int(in_shazam_charts),
        "bpm": int(bpm),
        "key": key,
        "mode": mode,
        "danceability": int(danceability),
        "valence": int(valence),
        "energy": int(energy),
        "acousticness": int(acousticness),
        "instrumentalness": int(instrumentalness),
        "liveness": int(liveness),
        "speechiness": int(speechiness)
    }

    try:
        response = requests.post(API_URL, json=input_data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            prediction = result.get("predicted_streams")
            if prediction is not None:
                st.success(f"### Predicted Streams: {prediction:,}")
                st.balloons()
            else:
                st.error("Prediction failed: Response did not contain 'predicted_streams'")
        else:
            try:
                error_detail = response.json().get("detail", response.text)
            except:
                error_detail = response.text
            st.error(f"Error from API (Status {response.status_code}): {error_detail}")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the backend. Please ensure the FastAPI server is running at http://127.0.0.1:8000")
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")