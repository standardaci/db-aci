from typing import List, Tuple
from .validation_job import ValidationJob, ValidationStage
from .validation_storage import ValidationStorage
import uuid

class QueryValidator:
    def __init__(self, storage: ValidationStorage):
        self.storage = storage

    def pre_facto_validate(self, dialog_context: List[str], query: str) -> Tuple[bool, str]:
        job_id = str(uuid.uuid4())
        job = ValidationJob(id=job_id, stage=ValidationStage.PRE_FACTO, dialog_context=dialog_context, query=query)
        self.storage.save_job(job)
        return True, job_id

    def post_facto_validate(self, job_id: str, generated_query: str) -> bool:
        job = self.storage.get_job(job_id)
        if not job:
            raise ValueError(f"No validation job found with id {job_id}")
        
        job.update_generated_query(generated_query)
        self.storage.save_job(job)
        
        return True

    def human_evaluate(self, job_id: str, evaluation: str):
        job = self.storage.get_job(job_id)
        if not job:
            raise ValueError(f"No validation job found with id {job_id}")
        
        job.update_evaluation(evaluation)
        self.storage.save_job(job)
