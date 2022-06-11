from ebonite import Ebonite, create_model
from ebonite.ext.flask import FlaskServer

import pickle
import sklearn
import pandas as pd


def load_obj(path):
    with open(path,"rb") as f:
        obj = pickle.load(f)
    return obj
model1 = load_obj('model.pkl')
transformer = load_obj('transformer.pkl')



class mymodel(object):
    def __init__(self,feat,model):
        self.transformer = load_obj('transformer.pkl')
        self.model = load_obj('model.pkl')
        #self.X = transformer.transform(data)
    def predict(self,data):
        data = pd.DataFrame(data, index=[0])
        X = self.transformer.transform(data)
        #return self.model.predict(X)
        predicted_churn = self.model.predict(X)[0]
        predicted_proba_churn = self.model.predict_proba(X)[0][0]
        return {"predicted_churn": str(predicted_churn),
                "predicted_proba_churn":str(predicted_proba_churn)}
        

model_new = mymodel(transformer,model1)


def run_my_model(data):
    return model_new.predict(data)

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

df = pd.DataFrame(data, index=[0])

model_new.predict(df)
