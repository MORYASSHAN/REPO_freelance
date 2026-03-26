import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os

# Create models directory if it doesn't exist
if not os.path.exists("models"):
    os.makedirs("models")

# Load dataset
try:
    df = pd.read_csv("data/student_scores.csv")
    print(f"Loaded dataset with {len(df)} rows.")
except FileNotFoundError:
    print("Error: data/student_scores.csv not found.")
    exit()

X = df[["study_hours", "attendance", "past_scores"]]
y = df["exam_score"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train models
models = {
    "Linear Regression": LinearRegression(),
    "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42)
}

best_model = None
best_r2 = -float("inf")

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"\n--- {name} Performance ---")
    print(f"Mean Absolute Error: {mae:.2f}")
    print(f"Mean Squared Error: {mse:.2f}")
    print(f"R2 Score: {r2:.4f}")
    
    if r2 > best_r2:
        best_r2 = r2
        best_model = model

# Save the best model
if best_model:
    print(f"\nSaving the best model (using {type(best_model).__name__}) to models/exam_predictor.pkl")
    joblib.dump(best_model, "models/exam_predictor.pkl")
    print("Model trained and saved successfully!")
else:
    print("No model was trained.")