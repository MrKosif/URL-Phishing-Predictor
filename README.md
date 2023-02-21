# URL Phishing Predictor

<img src="/readme/best-practices-phishing-protection.jpeg" align="left" width="192px" height="192px"/>
<img align="left" width="0" height="192px" hspace="10"/>

> This project is created for detecting phishing websites using it's URLs.

> URL Phishing Detector is a neural classifier model used to predict if a website is used for phishing attacks. It contains an advanced model alongside with basic model to predict the most accurate results with a small drawback. It's currently used by the fraud & abuse team in a company. 
<br>
<br>


## Installing the Required Libraries

```sh
$ pip3 install requirements.txt
```

# Getting Started

The phishing URL detector is a tool for detecting phishing URLs before they cause severe damage. It was created for a company which is selling mailing services that can be abused for phishing attacks. So, this classifier is getting used by fraud & abuse departments to prevent such attacks. In development, a dataset containing 10.000 URLs is created. The extracted features are divided into two major categories: URL features and page rank features. Page rank features are used in the advanced model for %8 improved accuracy with the drawback of waiting 30 seconds for each prediction. A deep neural network is used for creating a predictor classifier. Various data science libraries like Keras, Scikit-learn, NumPy, and Pandas are used in the implementation process. Finally, the Streamlit library is used for generating an easy-to-use user interface.


## Launch the Application

```sh
$ streamlit run ui.py
```

## Usage
Manuel URL Steps:
  1. Enter a URL you want to test.
  2. Check the box If you want the advanced search.
<img src="/readme/manuel.png" width="720px" height="338px"/>


File Upload Steps:
  1. Make sure your column name for the URL is "url".
  2. Upload your CSV file.
  3. Check the box If you want the advanced search.
<img src="/readme/file.png" width="720px" height="338px"/>
