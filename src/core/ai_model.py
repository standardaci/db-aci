from abc import ABC, abstractmethod
from typing import Dict, Any

class AIModel(ABC):
    @abstractmethod
    def generate_query(self, natural_language_query: str, schema: Dict[str, Any], api_reference: str) -> str:
        pass
