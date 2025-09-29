import pickle
import pandas as pd
from fastapi import FastAPI, Request
from pydantic import BaseModel
import logging
# New imports for the exception handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

# Configure logging
logging.basicConfig(filename='predictions.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

# --- NEW EXCEPTION HANDLER ---
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logging.error(f"Validation error for request to {request.url}: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )

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

# The predict endpoint is now simpler as we don't need the try/except
@app.post("/predict")
def predict(data: IrisInput):
    if model is None:
        return {"error": "Model not loaded. Please train the model first."}

    input_df = pd.DataFrame([data.dict()])
    input_df.columns = ['sepal.length', 'sepal.width', 'petal.length', 'petal.width']
    
    prediction = model.predict(input_df)[0]
    logging.info(f"Prediction successful for input {data.dict()}. Result: {prediction}")
    return {"prediction": prediction}