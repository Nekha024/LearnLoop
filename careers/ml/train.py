import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# --- Configuration ---
# This is the updated CSV file you uploaded.
DATA_FILE = "Career-prediction-data.csv" 

# These are the output files.
MODEL_FILE = "career_model.pkl"
ENCODERS_FILE = "encoders.pkl"
# ---------------------

print(f"Loading data from {DATA_FILE}...")
if not os.path.exists(DATA_FILE):
    print(f"Error: Data file not found at {DATA_FILE}")
    print("Please make sure your updated CSV file is in the same directory as this script.")
else:
    df = pd.read_csv(DATA_FILE)

    # Encode categorical columns
    label_encoders = {}
    print("Encoding categorical columns...")
    for column in df.columns:
        if df[column].dtype == 'object':
            le = LabelEncoder()
            df[column] = le.fit_transform(df[column])
            label_encoders[column] = le
            # print(f" - Encoded column: {column}")

    # Split features & target
    X = df.drop("Suggested Job Role", axis=1)
    y = df["Suggested Job Role"]

    # Train test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Model
    print("Training RandomForestClassifier model...")
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    # Save model & encoders
    joblib.dump(model, MODEL_FILE)
    joblib.dump(label_encoders, ENCODERS_FILE)

    print("\n--- Success! ---")
    print(f"New model saved to: {MODEL_FILE}")
    print(f"New encoders saved to: {ENCODERS_FILE}")
    print("\nNext steps:")
    print(f"1. Copy {MODEL_FILE} and {ENCODERS_FILE} to your Django project's folder:")
    print("   (e.g., /learnloop/careers/ml/)")
    print("2. Restart your Django server.")
