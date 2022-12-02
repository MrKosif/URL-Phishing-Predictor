from decimal import DivisionUndefined
from distutils.command.upload import upload
import numpy as np
import pandas as pd
import streamlit as st
import random
from pickle import load
from tensorflow.keras.models import load_model

from feature_extractor import Extraction, FeatureFunctions
from data_prep import DataPrep
from predictions import Prediction

e = Extraction()
dp = DataPrep()
p = Prediction()


uploaded = False
file = False
text_box = False
predicted_df = None
advanced = False

def write_urls(array):
    with placeholder.container():
        for arr in array:
            original_title = f'<p style="font-family:IBM Plex Sans; color:Green; font-size: 15px;">{arr}</p>'
            st.markdown(original_title, unsafe_allow_html=True)

def start_prediction(dataframe):
    urls = dataframe["url"]
    try:
        if advanced: # if advanced true
            features = e.main(advanced=True, urls=urls)
            prep_data = dp.main(features)
            prediction = p.predict(prep_data)
            pred = prediction > 0.5
            dataframe["isPhishing"] = pred.reshape(-1).astype("str")
            #dataframe["prediction"] = np.round(np.resize(prediction, (prediction.shape[0])), 3)
            return dataframe

        else:
            feature_df = e.main(advanced=False, urls=urls)
            dp.outlier("url_len", feature_df)
            pipeline = load(open('data/fast_pipeline.pkl', 'rb'))
            X_testp = pipeline.transform(feature_df)
            model = load_model("data/fast_model.h5")
            prediction = model.predict(X_testp)
            pred = prediction > 0.5
            dataframe["isPhishing"] = pred.reshape(-1).astype("str")
            #dataframe["prediction"] = dataframe["prediction"] > 0.5
            #dataframe["prediction"] = np.round(np.resize(prediction, (prediction.shape[0])), 3)
            return dataframe

    except DivisionUndefined:# IndexError:
            
        st.warning("Please include http-https tags!")
        # İnput box ile prediction yapacaksın


st.set_page_config(layout="wide",
                   page_title="Real-Time Data Science Dashboard",)

col1, col2, col3 = st.columns([5, 5, 20])
with col3:
    st.title("Spam URL Detector")


col1, col2, col3 = st.columns([7, 20, 5])
with col2:
    placeholder = st.empty()


with st.sidebar:
    length = 0
    st.header("Configure the Model")

    ### UPLOAD SECTION ####
    uploaded_file = st.file_uploader(label="Upload a csv file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        uploaded = True
        #write_urls(df["url"])
        length = df.shape[0]
        file = True

    else:
        st.warning("You need to upload a csv file.")
    ######################

    ### MANUEL INPUT #####
    manuel_input = st.text_input(
        placeholder="https://www.google.com",
        label="Enter Url Manually",
    )
    if manuel_input is not None:
        urls = manuel_input.split(",")
        if urls[0] != "":
            arr = np.array(urls)
            df = pd.DataFrame(arr, columns=["url"])
            if df.shape[0] > 1:
                length = df.shape[0]

    ######################
    try:
        advanced = st.checkbox("Advanced Search")
        #st.button(label= "Start Detection")
        if st.button("Start Detection"):
            predicted_df = start_prediction(df)
        
        if advanced == False:
            duration = round((length * 2.5)/60, 2)
            accuracy = "%87"
        elif advanced == True:
            duration = round((length * 35)/60, 2)
            accuracy = "%94"
        else:
            duration = "Unknown"
        time = st.text(f"Run time: around {duration} minutes")
        accuracy = st.text(f"Accuracy: around {accuracy}")

    except NameError:
        st.warning("Please Enter a valid input!")


col1, col2 = st.columns([3, 20])
with col2:
    if predicted_df is not None:
        st.dataframe(predicted_df[["url", "isPhishing"]], width=700)

