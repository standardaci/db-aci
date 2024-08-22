from typing import List, Dict, Any
from ..core.database_connector import DatabaseConnector
from ..core.ai_model import AIModel
from ..validation.query_validator import QueryValidator
from ..validation.api_call_validator import APICallValidator
import json

class QueryExecutor:
    def __init__(self, db_connector: DatabaseConnector, ai_model: AIModel, 
                 query_validator: QueryValidator, api_validator: APICallValidator):
        self.db_connector = db_connector
        self.ai_model = ai_model
        self.query_validator = query_validator
        self.api_validator = api_validator

    def execute_natural_language_query(self, nl_query: str, dialog_context: List[str] = []) -> List[Dict[Any, Any]]:
        schema = self.db_connector.get_schema()
        api_reference = self.load_api_reference()

        # Pre-facto validation
        is_valid, job_id = self.query_validator.pre_facto_validate(dialog_context, nl_query)
        if not is_valid:
            raise ValueError("Query did not pass pre-facto validation")

        generated_query = self.ai_model.generate_query(nl_query, schema, api_reference)

        # Post-facto validation
        if not self.query_validator.post_facto_validate(job_id, generated_query):
            raise ValueError("Query did not pass post-facto validation")

        # API call validation
        api_call = self.prepare_api_call(generated_query)
        is_valid_api, api_job_id = self.api_validator.validate_api_call(api_call)
        if not is_valid_api:
            raise ValueError("API call did not pass validation")

        # Execute the query
        results = self.db_connector.execute_query(generated_query)

        # Record API response
        self.api_validator.record_api_response(api_job_id, {"results": results})

        return results

    def load_api_reference(self) -> str:
        with open('api_reference.json', 'r') as f:
            return json.load(f)

    def prepare_api_call(self, query: str) -> Dict[str, Any]:
        return {
            "method": "POST",
            "endpoint": "/execute_query",
            "body": {"query": query}
        }

    def undo_last_query(self) -> bool:
        jobs = self.api_validator.storage.get_jobs_by_stage(ValidationStage.API_CALL)
        if not jobs:
            return False
        
        last_job = max(jobs, key=lambda j: j.created_at)
        return self.api_validator.undo_api_call(last_job.id)
