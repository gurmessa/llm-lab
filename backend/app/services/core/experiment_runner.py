from metrics.overall_metric import OverallMetric
from services.llm.constants import DEFAULT_OPENAI_MODEL_NAME
from services.llm.openai_responder import OpenAIResponder


class ExperimentRunner:
    """Facade class to handle running the full experiment:
    1. Get response from LLM
    2. Calculate overall metrics
    3. Return combined result
    """

    def __init__(
        self, model_name: str = DEFAULT_OPENAI_MODEL_NAME, metrics_list: list = None
    ):
        self.model_name = model_name
        self.responder = OpenAIResponder(model_name=model_name)
        self.metric = OverallMetric(metrics_list=metrics_list)

    def run(self, user_prompt: str) -> dict:
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
        response = self.responder.get_response(user_prompt)

        # 2. Calculate overall metrics
        score_dict = self.metric.evaluate(response)

        # 3. Return combined result
        return {"llm_response": response, "metrics": score_dict}
