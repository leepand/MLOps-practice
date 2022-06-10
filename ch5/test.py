from model_manage import ModelManager
model_manager = ModelManager()
model_manager.load_models(configuration= [{"module_name":
                                           "churn_model",
                                           "class_name": "ChurnModel"}])
model_manager.get_models()
