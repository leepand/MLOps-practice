import importlib
from churn_model.base import ModelBase

class ModelManager(object): 
    """用于实例化和管理模型对象的单例类""" 
    models = []
    @classmethod
    def load_models(cls, configuration):
        for c in configuration:
            model_module = importlib.import_module(c["module_name"])
            model_class = getattr(model_module, c["class_name"])
            model_object = model_class()
            if isinstance(model_object, ModelBase) is False:
                raise ValueError("ModelManager 仅管理对 ModelBase 类型对象的引用")
            cls.models.append(model_object)
    
    @classmethod
    def get_models(cls):
        """从模型管理实例中获取模型信息列表""" 
        model_objects = [{
            "display_name": model.display_name,
            "qualified_name": model.qualified_name,
            "description": model.description,
            "model_version":model.version,
            "major_version": model.major_version,
            "minor_version": model.minor_version}  for model in cls.models]
        return model_objects
    @classmethod
    def get_model(cls, qualified_name):
        """通过 qualified_name 获取模型对象"""
        # 从模型对象列表中获取满足要求的模型
        model_objects = [model for model in cls.models if
                         model.qualified_name == qualified_name]
        if len(model_objects) == 0:
            return None
        else:
            return model_objects[0]
