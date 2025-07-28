import json

def extract_tables_prompt(tables_names: list[str], question: str) -> str:
    # Format the list as a string
    tables_text = "\n".join(f"- {name}" for name in tables_names)

    prompt = f"""
    You are an assistant that helps decide which tables from the user's available tables
    need to be checked to answer the user's question.

    User's tables:
    {tables_text}

    User's question:
    {question}

    Instructions:
    - Return only a JSON array of table names that are relevant to the question.
    - If you do not understand the question or no tables are relevant, return an empty JSON array [].
    - Do not add any other text or explanation, only return the JSON array.
    - The spape of data that you should return : [{{"id":"id of table", "name":"name of table"}}, ...]
    """

    return prompt


def get_answer_prompt(table_data: dict, user_question: str) -> str:
    # Convert table_data dict to pretty JSON string to include in the prompt
    table_json_str = json.dumps(table_data, indent=2, ensure_ascii=False)

    prompt = f"""
    You are an expert data assistant.

    You have access to the following table data in JSON format:
    {table_json_str}

    User's question:
    {user_question}

    Instructions:
    - Provide a formal, polite, and clear answer in English to the user's question under the key "answer".
    - Also provide a list of SQL queries under the key "sql_queries" that are needed to fulfill the user's request.
    - The SQL queries can be SELECT, INSERT, UPDATE, or DELETE statements depending on the user's needs.
    - If the user request requires calculations like average, sum, count, or data analysis, answer the question yourself using the data provided (no need to generate SQL for calculations).
    - Do not provide any extra explanations about calculations or queries; the user only needs a natural, straightforward answer.
    - If you understand, say to the user at the beginning of your answer that you have understood.
    - Do not give any extra explanations.
    - If you do not understand the user's request, respond with the answer:
    "Unfortunately, I did not understand your request. Please try again."
    - Return your entire response only as a JSON object with exactly two keys: "answer" and "sql_queries".
    - Do not add any explanation or text outside the JSON object.

    Example output:
    {{
    "answer": "Your formal and polite answer here.",
    "sql_queries": ["SELECT * FROM table WHERE ...;", "UPDATE table SET ...;"]
    }}
    """
    print(prompt)
    return prompt


