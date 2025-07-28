from openai import OpenAI
from core.config import settings
from services.rag_builder import extract_tables_prompt
from core.logger import logger

Bot = OpenAI(api_key=settings.GPT_TOKEN)

def extract_tables_from_question(tables_names: list[str], question: str) -> list[str]:
    """
    This function asks ChatGPT which tables from the user's list should be checked
    to fulfill the user's request.

    Args:
        tables_names (list(str)): List of user table names.
        question (str): User's question or request.

    Returns:
        list[str]: List of table names ChatGPT considers relevant, or empty list if none.
    """

    # prepare prompt
    prompt = extract_tables_prompt(tables_names=tables_names, question=question)
    
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

        # Validate that it's a list of dicts with 'id' and 'name'
        if isinstance(tables_list, list) and all(
            isinstance(item, dict) and 'id' in item and 'name' in item
            for item in tables_list
        ):
            return tables_list
        else:
            return []

    except Exception as e:
        # In case of any error, return empty list and optionally log error
        logger.error(f"Error in extracting table names: {e}")
        return []
