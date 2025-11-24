from app.services.llm.constants import (
    DEFAULT_MAX_TOKENS,
    DEFAULT_OPENAI_MODEL_NAME,
    DEFAULT_TEMPERATURE,
    DEFAULT_TOP_P,
)
from app.services.llm.openai_responder import OpenAIResponder
from app.services.metrics.overall_metric import OverallMetric


class ExperimentRunner:
    """Facade class to handle running the full experiment:
    1. Get response from LLM
    2. Calculate overall metrics
    3. Return combined result
    """

    def __init__(
        self, model_name: str = DEFAULT_OPENAI_MODEL_NAME, metrics_list: list = None
    ):
        self.responder = OpenAIResponder(model=model_name)
        self.metric = OverallMetric()

    def run(
        self,
        user_prompt: str,
        temperature: float = DEFAULT_TEMPERATURE,
        top_p: float = DEFAULT_TOP_P,
        max_tokens: int = DEFAULT_MAX_TOKENS,
    ) -> dict:
        """
        Run the experiment for a given user prompt.
        Returns:
            dict: {
                "user_prompt": str,
                "llm_response": str,
                "metrics": dict
            }
        """

        # 1. Get LLM response
        response = self.responder.run(
            user_prompt,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
        )

        # 2. Calculate overall metrics
        score_dict = self.metric.compute(response, user_prompt)

        # 3. Return combined result
        return {"llm_response": response, "metrics": score_dict}
