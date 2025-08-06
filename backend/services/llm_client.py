from openai import OpenAI
from core.config import settings
import json
from services.rag_builder import main_prompt
from core.logger import logger

Bot = OpenAI(api_key=settings.GPT_TOKEN)

def get_answer(table_names: list, user_text: str):

    # prepare prompt
    prompt = main_prompt(table_names=table_names, user_text=user_text)

    try:
        response = Bot.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful and precise assistant and your name is Zap."},
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
            and "success" in result
            and "answer_sentence" in result
            and "queries" in result
            and isinstance(result["queries"], list)
        ):
            return result
        else:
            # Return fallback if invalid response structure
            return {
                "success": False,
                "answer_sentence": "Unfortunately, I did not understand your request. Please try again.",
                "queries": []
            }

    except Exception as e:
        logger.error(f"Error in LLM response parsing: {e}")
        return {
                "success": False,
                "answer_sentence": "Unfortunately, I did not understand your request. Please try again.",
                "queries": []
            }
