import pickle
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
import logging

# Configure logging
logging.basicConfig(filename='predictions.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

# Define the input data model
class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

# Load the trained model
try:
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
except FileNotFoundError:
    model = None
    logging.error("Model file (model.pkl) not found.")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Iris Prediction API"}

@app.post("/predict")
def predict(data: IrisInput):
    if model is None:
        logging.error("Prediction failed: Model is not loaded.")
        return {"error": "Model not loaded. Please train the model first."}

    # Create a DataFrame from the input
    input_df = pd.DataFrame([data.dict()])
    # Rename columns to match training data
    input_df.columns = ['sepal.length', 'sepal.width', 'petal.length', 'petal.width']

    try:
        # Get prediction
        prediction = model.predict(input_df)[0]
        logging.info(f"Prediction successful for input {data.dict()}. Result: {prediction}")
        return {"prediction": prediction}
    except Exception as e:
        logging.error(f"Prediction failed for input {data.dict()}. Error: {str(e)}")
        return {"error": str(e)}