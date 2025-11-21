from abc import ABC, abstractmethod


class Metric(ABC):
    @abstractmethod
    def compute(self, llm_response: str, user_prompt: str = None) -> float:
        """Compute metric score. User prompt is optional."""
        pass
