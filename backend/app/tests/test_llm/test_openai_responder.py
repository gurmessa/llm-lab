import pytest

from ...services.llm.openai_responder import OpenAIResponder


@pytest.mark.skip(reason="Tested it once, no need to run it every time.")
def test_openai_responder():
    responder = OpenAIResponder()
    prompt = "Hello! Give me a short friendly greeting."

    response = responder.run(prompt, temperature=1, top_p=1.0, max_tokens=5)

    print("OpenAI response:", response)
    assert isinstance(response, str)
    assert len(response) > 0


def test_raise_model_not_allowed_error():
    with pytest.raises(Exception) as excinfo:
        OpenAIResponder(model="invalid-model")
    assert "is not allowed" in str(excinfo.value)
