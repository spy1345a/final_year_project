from numpy import vectorize
from loading import Load_Model,Load_Vectorizer

def main():
    model = Load_Model("model/model.pkl",debug=True)
    vectorizer=Load_Vectorizer("model/vectorizer.pkl",debug=True)

    if model and vectorizer:
        print("--------ML IS ready to predict---------")
    

    text = "Enter Test text here"

    X = vectorizer.transform([text])
    prediction = model.predict(X)

    print("Input:", text)
    print("Prediction:", prediction[0])
if __name__ == "__main__":
    main()
