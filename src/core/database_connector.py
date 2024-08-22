from abc import ABC, abstractmethod
from typing import List, Dict, Any

class DatabaseConnector(ABC):
    @abstractmethod
    def execute_query(self, query: str) -> List[Dict[Any, Any]]:
        pass

    @abstractmethod
    def get_schema(self) -> Dict[str, Any]:
        pass
