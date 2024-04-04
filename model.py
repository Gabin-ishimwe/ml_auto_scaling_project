import pickle
import pandas as pd
def load_model():
    # Load your machine learning model using Pickle
    with open("model_2.pkl", "rb") as model_file:
        # model = pickle.load(model_file)
        model = pd.read_pickle(model_file)
    return model