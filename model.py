import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error,r2_score

# Load dataset
data=pd.read_csv(
    "spotify-2023.csv",
    encoding="latin-1"
)

# Remove commas from all columns
for col in data.columns:
    data[col]=data[col].astype(str).str.replace(",","")

# Convert numeric columns
for col in data.columns:
    data[col]=pd.to_numeric(
        data[col],
        errors="coerce"
    )

# Reload categorical columns from original dataset
raw=pd.read_csv(
    "spotify-2023.csv",
    encoding="latin-1"
)

cat_cols=[
    "track_name",
    "artist(s)_name",
    "key",
    "mode"
]

for col in cat_cols:
    data[col]=raw[col]

# Drop rows with missing values
data=data.dropna()

# Remove text-heavy columns
data=data.drop([
    "track_name",
    "artist(s)_name"
],axis=1)

# Encode categorical columns
data=pd.get_dummies(
    data,
    columns=["key","mode"],
    drop_first=True
)

# Features and target
X=data.drop("streams",axis=1)
y=data["streams"]

# Train test split
X_train,X_test,y_train,y_test=train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Model
model=LinearRegression()

# Train model
model.fit(X_train,y_train)

# Predictions
y_pred=model.predict(X_test)

# Metrics
mse=mean_squared_error(y_test,y_pred)
r2=r2_score(y_test,y_pred)

print("Mean Squared Error:",mse)
print("R2 Score:",r2)

from joblib import dump
dump(model,"spotify_model.joblib")
