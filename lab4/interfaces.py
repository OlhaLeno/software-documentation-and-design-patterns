from abc import ABC, abstractmethod
from typing import List, Dict, Any

class IOutputStrategy(ABC):
    """
    Abstract base class (Interface) for data output strategies.
    """
    @abstractmethod
    def output(self, data: List[Dict[str, Any]]) -> None:
        pass