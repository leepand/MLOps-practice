from pyjackson.decorators import make_string, type_field
import datetime

@make_string('id', 'name')
class Experiment(object):
    """
    Experiment is a collection of submodels

    :param id: experiment id
    :param name: experiment name
    :param author: user that created that experiment
    :param creation_date: date when this experiment was created
    """
    def __init__(self, name: str, 
                 id: int = None, 
                 author: str = None, 
                 experiment_remark: str = None,
                 experiment_sequence: int = None,
                 del_flag: int = None,
                 task_id: int = None,
                 creation_date: datetime.datetime = None):
        super().__init__(id, name, author, creation_date)
        self.experiment_remark="experiment_remark"
        self.experiment_sequence = experiment_sequence
        self.task_id = task_id
        self.del_flag = del_flag

@make_string('id', 'name')
class ModelMetric(object):
    """
    ModelMetric contains metadata for machine learning model's metrics

    :param name: metric name
    """

    PYTHON_VERSION = 'python_version'

    def __init__(self, name: str, 
                 metric_type: str = None,
                 metric_value: float = None,
                 epoch: int = None,
                 id: int = None,
                 experiment_id: int = None,
                 author: str = None, 
                 creation_date: datetime.datetime = None):
        super().__init__(id, name, author, creation_date)
        self.metric_type = metric_type
        self.metric_value = metric_value
        self.epoch =epoch
        self.experiment_id = experiment_id
        
        
@make_string('id', 'name')
class ModelParam(object):
    """
    ModelParam contains metadata for machine learning model's params

    :param name: param name
    """

    PYTHON_VERSION = 'python_version'

    def __init__(self, name: str, 
                 param_type: str = None,
                 param_value: float = None,
                 id: int = None,
                 experiment_id: int = None,
                 author: str = None, 
                 creation_date: datetime.datetime = None):
        super().__init__(id, name, author, creation_date)
        self.param_type = param_type
        self.param_value = param_value
        self.experiment_id = experiment_id      

@make_string('id', 'name')
class BestResult(object):
    """
    BestResult contains metadata for machine learning model's best result

    :param name: result name
    """

    PYTHON_VERSION = 'python_version'

    def __init__(self, name: str, 
                 best_epoch: int = None,
                 best_value: float = None,
                 id: int = None,
                 experiment_id: int = None,
                 author: str = None, 
                 creation_date: datetime.datetime = None):
        super().__init__(id, name, author, creation_date)
        self.best_epoch = best_epoch
        self.best_value = best_value
        self.experiment_id = experiment_id