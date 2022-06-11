from werkzeug.local import Local
import pandas as pd
import pickle
import sklearn

from .middleware import AfterResponse

app = Flask(__name__)
AfterResponse(app)
local = Local()

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

@app.route('/update-model', methods=['POST'])
def update_model():
    _cache = get_cache()
    new_path = request.args.get('model_path')
    busy_signal = int(_cache.get('busy_signal'))
    if not busy_signal:
        _cache.set('busy_signal', 1)
        load_model(new_path, _cache)
        _cache.set('busy_signal', 0)
    return jsonify({'状态': '模型更新成功!'})

@app.after_response
def check_cache():
    _cache = get_cache()
    global model
    cached_hash = _cache.get('model_hash')
    if model.hash != cached_hash:
        busy_signal = int(r.get('busy_signal'))
        if not busy_signal:
            # 如果空闲，我们将更新并第一时间将信号变量设置为1
            _cache.set('busy_signal', 1)
            model_location = _cache.get('model_location')
            load_model(model_location, _cache)
            _cache.set('busy_signal', 0)

def get_cache():
    cache = getattr(local, 'cache', None)
    if cache is None:
        local.cache = redis.Redis(decode_responses='utf-8')
    return local.cache

if __name__ == '__main__':
    app.run()
