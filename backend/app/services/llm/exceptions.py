class ModelNotAllowedError(Exception):
    """Exception raised when a llm model is not allowed."""

    pass


class OpenAIAPIError(Exception):
    """Exception raised for OpenAI API related errors."""

    pass
