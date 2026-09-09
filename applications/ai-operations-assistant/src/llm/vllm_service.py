"""vLLM OpenAI-compatible inference service."""

import os

import requests


DEFAULT_BASE_URL = "http://localhost:8000/v1"
DEFAULT_MODEL = "meta-llama/Llama-3.2-3B-Instruct"


class VLLMService:
    """Generate responses using a vLLM OpenAI-compatible API."""

    def __init__(
        self,
        base_url: str | None = None,
        model: str | None = None,
        timeout: int = 60,
    ) -> None:
        self.base_url = (
            base_url
            or os.getenv("VLLM_BASE_URL")
            or DEFAULT_BASE_URL
        ).rstrip("/")

        self.model = (
            model
            or os.getenv("VLLM_MODEL")
            or DEFAULT_MODEL
        )

        self.timeout = timeout

    def generate(self, prompt: str) -> str:
        """Send a prompt to vLLM and return the generated response."""

        if not isinstance(prompt, str):
            raise TypeError("prompt must be a string")

        cleaned_prompt = prompt.strip()

        if not cleaned_prompt:
            raise ValueError("prompt cannot be empty")

        response = requests.post(
            f"{self.base_url}/chat/completions",
            json={
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": cleaned_prompt,
                    }
                ],
                "temperature": 0.1,
            },
            timeout=self.timeout,
        )

        response.raise_for_status()

        data = response.json()

        return data["choices"][0]["message"]["content"].strip()