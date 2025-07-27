from openai import OpenAI
from core.config import settings

Bot = OpenAI(api_key=settings.GPT_TOKEN)

def extract_tables_from_question(tables_names: list[str], question: str) -> list[str]:
    """
    This function asks ChatGPT which tables from the user's list should be checked
    to fulfill the user's request.

    Args:
        tables_names (list[str]): List of user table names.
        question (str): User's question or request.

    Returns:
        list[str]: List of table names ChatGPT considers relevant, or empty list if none.
    """

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
    """

    try:
        response = Bot.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=200,
        )
        answer_text = response.choices[0].message.content.strip()

        # Attempt to parse the response as JSON list
        import json
        tables_list = json.loads(answer_text)

        # Validate that it is a list of strings
        if isinstance(tables_list, list) and all(isinstance(item, str) for item in tables_list):
            return tables_list
        else:
            # If format unexpected, return empty list
            return []

    except Exception as e:
        # In case of any error, return empty list and optionally log error
        print(f"Error in extracting table names: {e}")
        return []
