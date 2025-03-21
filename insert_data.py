import pandas as pd
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["crop_db"]
collection = db["crops"]

# Load dataset
df = pd.read_csv("Crop_recommendation.csv")

# Convert DataFrame to dictionary and insert into MongoDB
data = df.to_dict(orient="records")
collection.insert_many(data)

print("Data inserted successfully!")
