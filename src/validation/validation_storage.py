from typing import List, Optional
from .validation_job import ValidationJob, ValidationStage
import json
import os

class ValidationStorage:
    def __init__(self, storage_path: str):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)

    def save_job(self, job: ValidationJob):
        file_path = os.path.join(self.storage_path, f"{job.id}.json")
        with open(file_path, 'w') as f:
            json.dump(job.__dict__, f, default=str)

    def get_job(self, job_id: str) -> Optional[ValidationJob]:
        file_path = os.path.join(self.storage_path, f"{job_id}.json")
        if not os.path.exists(file_path):
            return None
        with open(file_path, 'r') as f:
            data = json.load(f)
            return ValidationJob(**data)

    def get_all_jobs(self) -> List[ValidationJob]:
        jobs = []
        for filename in os.listdir(self.storage_path):
            if filename.endswith(".json"):
                job_id = filename[:-5]  # Remove .json extension
                job = self.get_job(job_id)
                if job:
                    jobs.append(job)
        return jobs

    def get_jobs_by_stage(self, stage: ValidationStage) -> List[ValidationJob]:
        return [job for job in self.get_all_jobs() if job.stage == stage]
