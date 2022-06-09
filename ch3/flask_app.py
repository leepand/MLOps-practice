from flask import Flask, jsonify, request
import pandas as pd
import pickle
import sklearn
app = Flask(__name__)

def load_obj(path):
    with open(path,"rb") as f:
        obj = pickle.load(f)
    return obj
model = load_obj('model.pkl')
transformer = load_obj('transformer.pkl')
categories = ['PhoneService', 'Contract', 'PaperlessBilling', 
              'PaymentMethod', 'gender', 'Partner', 
              'Dependents', 'MultipleLines', 'InternetService',
              'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 
              'TechSupport', 'StreamingTV', 'StreamingMovies']
numerical = ['tenure', 'MonthlyCharges', 'TotalCharges','SeniorCitizen']
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    df = pd.DataFrame(data, index=[0])
    X = transformer.transform(df)
    predicted_churn = model.predict(X)[0]
    predicted_proba_churn = model.predict_proba(X)[0][0]
    return jsonify({"predicted_churn": str(predicted_churn),
                    "predicted_proba_churn":str(predicted_proba_churn)})

if __name__ == '__main__':
     app.run()
