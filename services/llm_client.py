from openai import OpenAI
from core.config import settings
import json
from services.rag_builder import get_answer_prompt

Bot = OpenAI(api_key=settings.GPT_TOKEN)

def get_answer_and_sql_queries(table_data: dict, user_question: str) -> dict:
    """
    Send the user's question along with the specific table data to the LLM,
    requesting a formal and polite answer and a list of SQL queries.

    Args:
        table_data (dict): Parsed JSON data of the target table.
        user_question (str): The user's natural language question.

    Returns:
        dict: {
            "answer": str,        # Formal polite answer or fallback message.
            "sql_queries": list   # List of SQL query strings to fulfill the request.
        }
    """

    # prepare prompt
    prompt = get_answer_prompt(table_data=table_data, user_question=user_question)

    try:
        response = Bot.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful and precise assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=600,
        )
        answer_text = response.choices[0].message.content.strip()

        # Parse the response JSON
        result = json.loads(answer_text)

        # Validate keys and types
        if (
            isinstance(result, dict)
            and "answer" in result
            and "sql_queries" in result
            and isinstance(result["answer"], str)
            and isinstance(result["sql_queries"], list)
            and all(isinstance(q, str) for q in result["sql_queries"])
        ):
            return result
        else:
            # Return fallback if invalid response structure
            return {
                "answer": "Unfortunately, I did not understand your request. Please try again.",
                "sql_queries": []
            }

    except Exception as e:
        print(f"Error in LLM response parsing: {e}")
        return {
            "answer": "Unfortunately, I did not understand your request. Please try again.",
            "sql_queries": []
        }
