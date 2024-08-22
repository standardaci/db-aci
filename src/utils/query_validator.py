import sqlparse

def validate_query(query: str) -> bool:
    parsed = sqlparse.parse(query)
    if not parsed:
        return False
    
    dangerous_keywords = ['DROP', 'DELETE', 'TRUNCATE', 'ALTER']
    for statement in parsed:
        for token in statement.tokens:
            if token.ttype is sqlparse.tokens.Keyword and token.value.upper() in dangerous_keywords:
                return False
    
    return True
