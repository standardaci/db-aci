from typing import Dict, Any, Tuple
from .validation_job import ValidationJob, ValidationStage
from .validation_storage import ValidationStorage

class APICallValidator:
    def __init__(self, storage: ValidationStorage):
        self.storage = storage

    def validate_api_call(self, api_call: Dict[str, Any]) -> Tuple[bool, str]:
        job = ValidationJob(
            stage=ValidationStage.API_CALL,
            dialog_context=[],
            query="",
            api_call=api_call
        )
        self.storage.save_job(job)
        return True, job.id

    def record_api_response(self, job_id: str, api_response: Dict[str, Any]):
        job = self.storage.get_job(job_id)
        if not job:
            raise ValueError(f"No validation job found with id {job_id}")
        
        job.update_api_call(job.api_call, api_response)
        self.storage.save_job(job)

    def undo_api_call(self, job_id: str) -> bool:
        job = self.storage.get_job(job_id)
        if not job or job.stage != ValidationStage.API_CALL:
            return False
        
        job.mark_as_undone()
        self.storage.save_job(job)
        return True
