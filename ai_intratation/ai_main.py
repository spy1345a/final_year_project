from .loading import Load_Model, Load_Vectorizer
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, "model", "model.pkl")
vectorizer_path = os.path.join(BASE_DIR, "model", "vectorizer.pkl")

model = Load_Model(model_path)
vectorizer = Load_Vectorizer(vectorizer_path)

def predict_text(text: str) -> dict:
    X = vectorizer.transform([text])
    prediction = model.predict(X)[0]  # extract the single result

    return {
        "input": text,
        "prediction": prediction
    }