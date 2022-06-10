from schema import Schema
from .base import ModelBase
import pickle
import pandas as pd
import os

display_name = "churn model"
description = "ML 模型接口标准化"
__qualified_name__ = __name__.split(".")[0]
__version_info__ = (0, 1, 0)
__version__ = ".".join([str(n) for n in __version_info__])


class ChurnModel(ModelBase):
    """ 演示如何使用 """
    qualified_name = __qualified_name__
    display_name = display_name
    description = description
    major_version = __version_info__[0]
    minor_version = __version_info__[1]
    version = __version__
    input_schema = Schema({'tenure': int,
                           'PhoneService': str,
                           'Contract': str,
                           'PaperlessBilling': str,
                           'PaymentMethod': str,
                           'MonthlyCharges':float,
                           'TotalCharges':float,
                           'gender':str,
                           'SeniorCitizen':int,
                           'Partner':str,
                           'Dependents':str,
                           'MultipleLines':str,
                           'InternetService':str,
                           'OnlineSecurity':str,
                           'OnlineBackup':str,
                           'DeviceProtection':str,
                           'TechSupport':str,
                           'StreamingTV':str,
                           'StreamingMovies':str
                          })
    # 模型的输出将是浮点类型
    output_schema = Schema({'predicted_proba_churn': 0.1 })
    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath("./"))
        file_model = open(os.path.join(dir_path, "model_files", "model.pkl"), 'rb')
        file_feat = open(os.path.join(dir_path, "model_files", "transformer.pkl"), 'rb')
        self._model = pickle.load(file_model)
        self._transformer = pickle.load(file_feat)
        file_model.close()
        file_feat.close()
    def predict(self, data):
        # 调用 super() 方法对输入模式进行验证
        super().predict(data=data)
        # 数据转换
        df = pd.DataFrame(data, index=[0])
        X = self._transformer.transform(df)
        # 进行预测，并将 scikit-learn 模型的输出转化为由输出模式所期望的浮点类型
        predicted_churn = self._model.predict(X)[0]
        predicted_proba_churn = self._model.predict_proba(X)[0][0]
        return {"predicted_proba_churn": predicted_proba_churn}

model = ChurnModel()
model.input_schema
model.output_schema
