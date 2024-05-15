from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import mlflow.pyfunc
from typing import List, Dict, Any
import pandas as pd

app = FastAPI()

# Define your Azure Blob Storage connection details
AZURE_STORAGE_ACCOUNT_NAME = "mlflowstorage1"
CONTAINER_NAME = "mlflow-artifacts"
BLOB_NAME = "artifacts"
# Keep this as a dynamic variable to fetch the latest model
RUN_ID = "1/2d3d191348084cf1af554baf130fe3c7/artifacts/SGDClassifier"

# Construct the Azure Blob Storage URI for MLflow
MODEL_URI = f"wasbs://{CONTAINER_NAME}@{AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net/{BLOB_NAME}/{RUN_ID}"

# Load the model from Azure Blob Storage
def load_model():
    model = mlflow.pyfunc.load_model(MODEL_URI)
    return model

# Define your prediction input schema
class PredictionInput(BaseModel):
    data: List[Dict[str, Any]]

# Load the model when the server starts
model = load_model()

@app.post("/predict")
def predict(input_data: PredictionInput):
    try:
        data = pd.DataFrame(input_data.data)
        prediction = model.predict(data)
        return {"prediction": prediction.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
