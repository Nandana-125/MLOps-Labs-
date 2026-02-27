from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from predict import predict_data

app = FastAPI()

class DiabetesInput(BaseModel):
    """
    Input features for diabetes risk prediction.
    All features are normalized float values from the sklearn diabetes dataset.
    """
    age: float
    sex: float
    bmi: float
    blood_pressure: float
    s1: float  # Total serum cholesterol
    s2: float  # Low-density lipoproteins
    s3: float  # High-density lipoproteins
    s4: float  # Total cholesterol / HDL
    s5: float  # Log of serum triglycerides
    s6: float  # Blood sugar level

class DiabetesResponse(BaseModel):
    prediction: int
    risk_level: str

@app.get("/", status_code=status.HTTP_200_OK)
async def health_check():
    """Health check endpoint to verify the API is running."""
    return {"status": "healthy", "model": "diabetes_risk_predictor"}

@app.post("/predict", response_model=DiabetesResponse)
async def predict_diabetes(features: DiabetesInput):
    """
    Predict diabetes risk based on health metrics.
    Returns:
        prediction: 0 (low risk) or 1 (high risk)
        risk_level: 'Low Risk' or 'High Risk'
    """
    try:
        input_data = [[
            features.age, features.sex, features.bmi,
            features.blood_pressure, features.s1, features.s2,
            features.s3, features.s4, features.s5, features.s6
        ]]
        prediction = predict_data(input_data)
        risk = "High Risk" if prediction[0] == 1 else "Low Risk"
        return DiabetesResponse(prediction=int(prediction[0]), risk_level=risk)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))