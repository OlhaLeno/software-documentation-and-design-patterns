from abc import ABC, abstractmethod

class IContentRepository(ABC):
    @abstractmethod
    def add(self, entity): pass

    @abstractmethod
    def commit(self): pass

class IFileService(ABC):
    @abstractmethod
    def get_data_from_file(self, path: str): pass