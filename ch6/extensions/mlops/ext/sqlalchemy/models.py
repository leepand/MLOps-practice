from sqlalchemy import (Column, DateTime, 
                        ForeignKey, Integer,
                        String, Text, 
                        UniqueConstraint, Float)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from abc import abstractmethod
from typing import Any, Dict, Iterable, List, Optional, Type, TypeVar
from .base import ModelParam,BestResult,ModelMetric,Experiment

SQL_OBJECT_FIELD = '_sqlalchemy_object'

T = TypeVar('T')
S = TypeVar('S', bound='Attaching')

class Attaching:
    id = ...
    name = ...

    def attach(self, obj):
        setattr(obj, SQL_OBJECT_FIELD, self)
        return obj

    @classmethod
    def from_obj(cls: Type[S], obj: T, new=False) -> S:
        kwargs = cls.get_kwargs(obj)
        existing = sqlobject(obj)
        if not new and existing is not None:
            update_attrs(existing, **kwargs)
            return existing
        return cls(**kwargs)

    @classmethod
    @abstractmethod
    def get_kwargs(cls, obj: T) -> dict:
        pass  # pragma: no cover

    @abstractmethod
    def to_obj(self) -> T:
        pass  # pragma: no cover


Base = declarative_base()

class SProject(Base, Attaching):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    author = Column(String, unique=False, nullable=False)
    creation_date = Column(DateTime, unique=False, nullable=False)

    tasks: Iterable['STask'] = relationship("STask", back_populates="project")
      
class STask(Base, Attaching):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=False, nullable=False)
    author = Column(String, unique=False, nullable=False)
    creation_date = Column(DateTime, unique=False, nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)

    project = relationship("SProject", back_populates="tasks")
    models: Iterable['SModel'] = relationship("SModel", back_populates="task")
    
    experiments: Iterable['TExperiment'] = relationship("TExperiment", back_populates='task')

    datasets = Column(Text)
    metrics = Column(Text)
    evaluation_sets = Column(Text)
    
class SModel(Base, Attaching):
    __tablename__ = 'models'

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String, unique=False, nullable=False)
    author = Column(String, unique=False, nullable=False)
    creation_date = Column(DateTime, unique=False, nullable=False)
    wrapper = Column(Text)

    artifact = Column(Text)
    requirements = Column(Text)
    description = Column(Text)
    params = Column(Text)
    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=False)
    task = relationship("STask", back_populates="models")

    evaluations = Column(Text)
class TExperiment(Base, Attaching):
    __tablename__ = 'experiments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=False, nullable=False)
    author = Column(String, unique=False, nullable=False)
    sub_model_remark = Column(String, unique=False, nullable=False)
    nick_name = Column(String, unique=False)
    sub_model_sequence = Column(Integer, nullable=False)
    del_flag = Column(Integer, default = 0)

    creation_date = Column(DateTime, unique=False, nullable=False)
    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=False)

    task = relationship("STask", back_populates="experiments")
    modelmetrics: Iterable['TModelmetric'] = relationship("TModelmetric", 
                                                           back_populates="experiment")
    modelparams: Iterable['TModelparam'] = relationship("TModelparam", 
                                                         back_populates="experiment")
    bestresult: Iterable['TBestresult'] = relationship("TBestresult", 
                                                        back_populates="experiment")

    __table_args__ = (UniqueConstraint('name', 'task_id', name='experiment_name_and_ref'),)

    def to_obj(self) -> Experiment:
        experiment = Experiment(
                        id=self.id,
                        name=self.name,
                        author=self.author,
                        creation_date=self.creation_date,
                        task_id=self.task_id,
                        experiment_remark=self.experiment_remark,
                        experiment_sequence=self.experiment_sequence)
    
class TModelmetric(Base, Attaching):
    __tablename__ = 'model_metrics'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=False, nullable=False)
    author = Column(String, unique=False, nullable=False)
    metric_type = Column(String, unique=False, nullable=False)
    metric_value = Column(Float, nullable=False)
    epoch = Column(Integer, nullable=False)

    creation_date = Column(DateTime, unique=False, nullable=False)
    experiment_id = Column(Integer, ForeignKey('experiments.id'), nullable=False)

    experiment = relationship("TExperiment", back_populates="modelmetrics")

    def to_obj(self) -> ModelMetric:
        modelmetric = ModelMetric(id=self.id,
                        name=self.name,
                        author=self.author,
                        creation_date=self.creation_date,
                        metric_type=self.metric_type,
                        metric_value=self.metric_value,
                        epoch=self.epoch,
                        experiment_id=self.experiment_id)
        return self.attach(modelmetric)

    @classmethod
    def get_kwargs(cls, model_metric: ModelMetric) -> dict:
        return dict(id=model_metric.id,
                    name=model_metric.name,
                    author=model_metric.author,
                    creation_date=model_metric.creation_date,
                    experiment_id=model_metric.experiment_id,
                    metric_type = model_metric.metric_type,
                    metric_value = model_metric.metric_value,
                    epoch = model_metric.epoch)
    
class TModelparam(Base, Attaching):
    __tablename__ = 'model_params'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=False, nullable=False)
    author = Column(String, unique=False, nullable=False)
    param_type = Column(String, unique=False, nullable=False)
    param_value = Column(String, nullable=False)

    creation_date = Column(DateTime, unique=False, nullable=False)
    experiment_id = Column(Integer, ForeignKey('experiments.id'), nullable=False)

    experiment = relationship("TExperiment", back_populates="modelparams")

    def to_obj(self) -> ModelParam:
        model_param = ModelParam(id=self.id,
                    name=self.name,
                    author=self.author,
                    creation_date=self.creation_date,
                    experiment_id=self.experiment_id,
                    param_type=self.param_type,
                    param_value=self.param_value)
        return self.attach(model_param)

    @classmethod
    def get_kwargs(cls, model_param: ModelParam) -> dict:
        return dict(id=model_param.id,
                    name=model_param.name,
                    author=model_param.author,
                    creation_date=model_param.creation_date,
                    experiment_id=model_param.experiment_id,
                    param_type = model_param.param_type,
                    param_value = model_param.param_value)
    
class TBestresult(Base, Attaching):
    __tablename__ = 'best_result'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=False, nullable=False)
    author = Column(String, unique=False, nullable=False)
    best_value = Column(Float, nullable=False)
    best_epoch = Column(Integer, nullable=False)

    creation_date = Column(DateTime, unique=False, nullable=False)
    experiment_id = Column(Integer, ForeignKey('experiments.id'), nullable=False)

    experiment = relationship("TExperiment", back_populates="bestresult")

    def to_obj(self) -> BestResult:
        best_result = BestResult(id=self.id,
                    name=self.name,
                    author=self.author,
                    creation_date=self.creation_date,
                    best_value=self.best_value,
                    best_epoch=self.best_epoch,
                    experiment_id=self.experiment_id)

        return self.attach(best_result)

    @classmethod
    def get_kwargs(cls, best_result: BestResult) -> dict:
        return dict(id=best_result.id,
                    name=best_result.name,
                    author=best_result.author,
                    creation_date=best_result.creation_date,
                    best_value=best_result.best_value,
                    best_epoch = best_result.best_epoch,
                    experiment_id = best_result.experiment_id)
