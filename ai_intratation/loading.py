from joblib import load

# Loading ML Model
def Load_Model(path, debug=False):
    print("-----------Loading ML model-----------")
    try:
        model = load(path)
        print("ML Model Loading Done")
        return model
    except Exception as e:
        print("ML Model Loading Failed")
        if debug:
            print(e)
        raise


def Load_Vectorizer(path, debug=False):
    print("-----------Loading Vectorizer-----------")
    try:
        vectorizer = load(path)
        print("Vectorizer Loading Done")
        return vectorizer
    except Exception as e:
        print("Vectorizer Loading Failed")
        if debug:
            print(e)
        raise


# -------------------------
# Local test (runs only if this file is executed)
# -------------------------
if __name__ == "__main__":
    print("Running loading.py self-test")

    model = Load_Model("model/model.pkl", debug=True)
    vectorizer = Load_Vectorizer("model/vectorizer.pkl", debug=True)

    print("Self-test completed successfully")