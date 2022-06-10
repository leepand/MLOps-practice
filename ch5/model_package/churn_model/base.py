from abc import ABC, abstractmethod

class ModelBase(ABC):
    """ML 模型预测代码(分析器)的一个抽象基类"""
    @property
    @abstractmethod
    def display_name(self) -> str:
        raise NotImplementedError()

    @property
    @abstractmethod
    def qualified_name(self) -> str:
        raise NotImplementedError()
        
    @property
    @abstractmethod
    def description(self) -> str:
        raise NotImplementedError()

    @property
    @abstractmethod
    def version(self) -> str:
        raise NotImplementedError()

    @property
    @abstractmethod
    def input_schema(self):
        raise NotImplementedError()
        
    @property
    @abstractmethod
    def output_schema(self):
        raise NotImplementedError()

    @abstractmethod
    def __init__(self):
        raise NotImplementedError()

    @abstractmethod
    def predict(self, data):
        self.input_schema.validate(data)
