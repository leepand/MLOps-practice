from sqlalchemy import (Column, DateTime, 
                        ForeignKey, Integer,
                        String, Text, 
                        UniqueConstraint, Float)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from abc import abstractmethod
from typing import Any, Dict, Iterable, List, Optional, Type, TypeVar

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
    pipelines: Iterable['SPipeline'] = relationship("SPipeline", back_populates='task')
    images: Iterable['SImage'] = relationship("SImage", back_populates='task')
    
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
    model_metrics: Iterable['TModelmetric'] = relationship("TModelmetric", back_populates="experiment")
    model_params: Iterable['TModelparam'] = relationship("TModelparam", back_populates="experiment")
    best_result: Iterable['TBestresult'] = relationship("TBestresult", back_populates="experiment")
