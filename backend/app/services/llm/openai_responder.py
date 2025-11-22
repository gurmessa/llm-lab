import os

from dotenv import load_dotenv
from openai import APIError, APIStatusError, APITimeoutError, OpenAI, RateLimitError

from .constants import (
    ALLOWED_OPENAI_MODELS,
    DEFAULT_MAX_TOKENS,
    DEFAULT_TEMPERATURE,
    DEFAULT_TOP_P,
    OPEN_AI_GPT_4_1_NANO,
)
from .exceptions import ModelNotAllowedError, OpenAIAPIError

load_dotenv()


class OpenAIResponder:
    def __init__(self, model: str = OPEN_AI_GPT_4_1_NANO):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        if model not in ALLOWED_OPENAI_MODELS:
            raise ModelNotAllowedError(f"Model {model} is not allowed.")

    def run(
        self,
        prompt: str,
        temperature: float = DEFAULT_TEMPERATURE,
        top_p: float = DEFAULT_TOP_P,
        max_tokens: int = DEFAULT_MAX_TOKENS,
    ) -> str:

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens,
            )

            return response.choices[0].message.content

        except (APIError, APIStatusError, APITimeoutError, RateLimitError) as e:
            raise OpenAIAPIError(f"OpenAI API error: {str(e)}")
        except Exception as e:
            raise e
