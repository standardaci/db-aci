from src.core.query_executor import QueryExecutor
from src.connectors.postgresql_connector import PostgreSQLConnector
from src.models.basic_llm_model import BasicLLMModel
from src.validation.query_validator import QueryValidator
from src.validation.api_call_validator import APICallValidator
from src.validation.validation_storage import ValidationStorage

def main():
    db_connector = PostgreSQLConnector("postgresql://username:password@localhost/dbname")
    ai_model = BasicLLMModel()
    validation_storage = ValidationStorage("./validation_data")
    query_validator = QueryValidator(validation_storage)
    api_validator = APICallValidator(validation_storage)
    executor = QueryExecutor(db_connector, ai_model, query_validator, api_validator)

    nl_query = "Find all users who joined in the last month"
    dialog_context = ["Hello, I'm looking for recent user data."]
    
    try:
        results = executor.execute_natural_language_query(nl_query, dialog_context)
        print(f"Query results: {results}")
        
        jobs = validation_storage.get_jobs_by_stage(ValidationStage.POST_FACTO)
        if jobs:
            query_validator.human_evaluate(jobs[0].id, "The query accurately reflected the user's request.")

        print("Attempting to undo the last query...")
        if executor.undo_last_query():
            print("Undo successful!")
        else:
            print("Undo failed.")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
