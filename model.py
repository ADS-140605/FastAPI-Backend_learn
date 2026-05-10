import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.preprocessing import LabelEncoder
from joblib import dump

# Load dataset
data = pd.read_csv("spotify-2023.csv", encoding="latin-1")

def clean_numeric(val):
    if isinstance(val, str):
        return val.replace(",", "")
    return val

# Clean problematic numeric columns
cols_to_fix = ["streams", "in_deezer_playlists", "in_shazam_charts"]
for col in cols_to_fix:
    data[col] = data[col].apply(clean_numeric)
    data[col] = pd.to_numeric(data[col], errors="coerce")

# Drop rows where target 'streams' is NaN
data = data.dropna(subset=["streams"])

# Feature Engineering: Total Playlists
data["total_playlists"] = (
    data["in_spotify_playlists"] + 
    data["in_apple_playlists"] + 
    data["in_deezer_playlists"].fillna(0)
)

# Encoding categorical features
le_key = LabelEncoder()
data["key"] = le_key.fit_transform(data["key"].astype(str))

le_mode = LabelEncoder()
data["mode"] = le_mode.fit_transform(data["mode"].astype(str))

# Select features
features = [
    "artist_count", "released_year", "released_month",
    "in_spotify_playlists", "in_spotify_charts",
    "in_apple_playlists", "in_apple_charts",
    "in_deezer_playlists", "in_deezer_charts",
    "in_shazam_charts", "total_playlists",
    "bpm", "key", "mode",
    "danceability_%", "valence_%", "energy_%",
    "acousticness_%", "instrumentalness_%", "liveness_%", "speechiness_%"
]

X = data[features]
y = data["streams"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model: HistGradientBoostingRegressor is often better than Random Forest
# and natively handles NaN/categorical if we specify them (though we pre-encoded)
model = HistGradientBoostingRegressor(
    max_iter=200, 
    learning_rate=0.05, 
    max_depth=5, 
    random_state=42
)

# Train
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Metrics
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Final Model Results:")
print(f"RMSE: {rmse:,.0f}")
print(f"MAE:  {mae:,.0f}")
print(f"R2:   {r2:.4f}")

# Save model and encoders
artifacts = {
    "model": model,
    "le_key": le_key,
    "le_mode": le_mode,
    "features": features
}
dump(artifacts, "spotify_model.joblib")
print("\n'Perfect' model and encoders saved to 'spotify_model.joblib'")
