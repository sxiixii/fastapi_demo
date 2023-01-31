from abc import ABC, abstractmethod


class BaseDB(ABC):
    @abstractmethod
    def get(self, *args, **kwargs):
        pass


class BaseCache(ABC):
    @abstractmethod
    def get(self, *args, **kwargs):
        pass

    @abstractmethod
    def put(self, *args, **kwargs):
        pass
