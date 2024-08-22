from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime
import uuid

class ValidationStage(Enum):
    PRE_FACTO = "pre_facto"
    POST_FACTO = "post_facto"
    API_CALL = "api_call"

@dataclass
class ValidationJob:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    stage: ValidationStage
    dialog_context: List[str]
    query: str
    generated_query: Optional[str] = None
    api_call: Optional[Dict[str, Any]] = None
    api_response: Optional[Dict[str, Any]] = None
    human_evaluation: Optional[str] = None
    is_undone: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def update_evaluation(self, human_evaluation: str):
        self.human_evaluation = human_evaluation
        self.updated_at = datetime.now()

    def update_generated_query(self, generated_query: str):
        self.generated_query = generated_query
        self.updated_at = datetime.now()

    def update_api_call(self, api_call: Dict[str, Any], api_response: Dict[str, Any]):
        self.api_call = api_call
        self.api_response = api_response
        self.updated_at = datetime.now()

    def mark_as_undone(self):
        self.is_undone = True
        self.updated_at = datetime.now()
