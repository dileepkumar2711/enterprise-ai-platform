import io
import json
#import json
#from unittest.mock import patch
from unittest.mock import patch

import pytest

from src.llm.ollama_service import OllamaService


class FakeResponse:
    """Simulate the HTTP response returned by Ollama."""

    def __init__(self, payload: dict):
        self._data = json.dumps(payload).encode("utf-8")

    def read(self):
        return self._data

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False


def test_generate_returns_ollama_response():
    service = OllamaService()

    fake_response = FakeResponse(
        {"response": "Azure Key Vault securely stores secrets."}
    )

    with patch(
        "src.llm.ollama_service.urllib.request.urlopen",
        return_value=fake_response,
    ):
        answer = service.generate("Where should I store secrets?")

    assert answer == "Azure Key Vault securely stores secrets."


def test_generate_rejects_empty_prompt():
    service = OllamaService()

    with pytest.raises(ValueError, match="Prompt cannot be empty"):
        service.generate("   ")


def test_generate_rejects_non_string_prompt():
    service = OllamaService()

    with pytest.raises(TypeError, match="Prompt must be a string"):
        service.generate(None)