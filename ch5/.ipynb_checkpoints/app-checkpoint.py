""" 基于flask创建的简单rest api. """
import os
from flask import Flask
from flask import jsonify, request, Response
from model_manage import ModelManager

import traceback

app = Flask(__name__)

MODELS = [
    {
        "module_name": "churn_model",
        "class_name": "ChurnModel"
    }
]

@app.route("/api/models/<qualified_name>/predict", methods=['POST'])
def predict(qualified_name):

    # 尝试反序列化JSON对象
    try:
        data = json.loads(request.data)
    except json.decoder.JSONDecodeError as e:
        response = dict(type="DESERIALIZATION_ERROR", message=str(e))
        response_data = error_schema.dumps(response).data
        return Response(response_data, status=400, mimetype='application/json')

    # 从 ModelManager中获取模型对象
    model_manager = ModelManager()
    model_object = model_manager.get_model(qualified_name=qualified_name)

    # 如果模型不存在返回 404
    if model_object is None:
        response = dict(type="ERROR", message="Model not found.")
        response_data = error_schema.dumps(response).data
        return Response(response_data, status=404, mimetype='application/json')

    try:
        prediction = model_object.predict(data)
        return jsonify(prediction), 200
    except Exception as e:
        traceback.print_exc()

    except Exception as e:
        response = dict(type="ERROR", message="Could not make a prediction.")
        response_data = error_schema.dumps(response).data
        return Response(response_data, status=500, mimetype='application/json')

@app.before_first_request
def instantiate_model_manager():
    """ 这个函数在应用程序启动时运行，它加载在配置中发现的所有模型。"""
    model_manager = ModelManager()
    model_manager.load_models(configuration= MODELS)
    
if __name__ == '__main__':
     app.run()