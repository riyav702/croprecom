from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["crop_db"]
collection = db["crops"]

# Load data from MongoDB
df = pd.DataFrame(list(collection.find({}, {"_id": 0})))

# Prepare data for ML model
X = df.drop(columns=["label"])
y = df["label"]

# Train model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save model
pickle.dump(model, open("crop_model.pkl", "wb"))

# Load saved model
model = pickle.load(open("crop_model.pkl", "rb"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get input values from form
        data = [float(request.form[key]) for key in ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]]

        # Predict crop
        prediction = model.predict([data])[0]

        return jsonify({"crop": prediction})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
