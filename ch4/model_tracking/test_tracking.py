import os
from random import random, randint
from tracking_core import  ModelTrack

model_track = ModelTrack(task_name="churn_model_mlops",task_desc = "流失模型研究")


if __name__ == "__main__":

    model_track.log_model_name("model-A")
    model_track.log_model_desc("模型-A")
    # Log a parameter (key-value pair)
    model_track.log_param({"param1" : randint(0, 100)},param_type = "logistic_param")

    # Log a metric; metrics can be updated throughout the run
    model_track.log_metric("foo", random(), epoch=1,is_best=0)
    model_track.log_metric("foo", random() + 1, epoch=1,is_best=0)
    model_track.log_metric("foo", random() + 2, epoch=1,is_best=0)
