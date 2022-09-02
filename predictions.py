import numpy as np
import pandas as pd
from pickle import load
from tensorflow.keras.models import load_model

class Prediction:

    def predict(self, dataframe):
        df = dataframe.copy()
        df["Crawled Flag"] = df["Crawled Flag"].astype(object)

        pipeline = load(open('data/pipeline.pkl', 'rb'))
        X_testp = pipeline.transform(df)

        model = load_model("data/model.h5")
        prediction = model.predict(X_testp)
        return prediction

#t_df = pd.read_csv("output/jotform_test.csv")
#url = t_df["url"][:49]
#df2 = pd.DataFrame()
#df2["url"] = url
#df2["result"] = prediction
#df2.to_csv("output/results.csv", index=False)