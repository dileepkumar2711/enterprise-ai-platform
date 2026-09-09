from unittest.mock import Mock, patch

import pytest

from src.llm.vllm_service import VLLMService


def test_generate_returns_vllm_response():
    service = VLLMService(
        base_url="http://vllm-server:8000/v1",
        model="test-model",
    )

    mock_response = Mock()
    mock_response.json.return_value = {
        "choices": [
            {
                "message": {
                    "content": "Azure Key Vault."
                }
            }
        ]
    }

    with patch(
        "src.llm.vllm_service.requests.post",
        return_value=mock_response,
    ) as mock_post:
        answer = service.generate(
            "Where should I securely store application passwords?"
        )

    assert answer == "Azure Key Vault."

    mock_post.assert_called_once()

    mock_response.raise_for_status.assert_called_once()


def test_generate_rejects_empty_prompt():
    service = VLLMService()

    with pytest.raises(ValueError):
        service.generate("   ")