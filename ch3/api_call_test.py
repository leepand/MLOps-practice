import requests
import json

url = 'http://127.0.0.1:5000/predict'
data ={"tenure":1,
         "PhoneService":"No",
         "Contract":"Month-to-month",
         "PaperlessBilling":"Yes",
         "PaymentMethod":"Electronic check",
         "MonthlyCharges":29.85,
         "TotalCharges":29.85,
         "gender":"Female",
         "SeniorCitizen":0,
         "Partner":"Yes",
         "Dependents":"No",
         "MultipleLines":"No phone service",
         "InternetService":"DSL",
         "OnlineSecurity":"No",
         "OnlineBackup":"Yes",
         "DeviceProtection":"No",
         "TechSupport":"No",
         "StreamingTV":"No",
         "StreamingMovies":"No"}
response = requests.post(url, json = data)
response.json()