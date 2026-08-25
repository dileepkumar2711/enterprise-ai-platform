"""Local LLM service using Ollama."""

import json
import os
import urllib.error
import urllib.request


class OllamaService:
    """Generate text using a locally running Ollama model."""

    def __init__(
        self,
        model: str = "llama3.2:3b",
        base_url: str | None = None,
    ) -> None:
        self.model = model
        self.base_url = (
            base_url
            or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        ).rstrip("/")

    def generate(self, prompt: str) -> str:
        """Generate one response from the configured Ollama model."""

        if not isinstance(prompt, str):
            raise TypeError("Prompt must be a string")

        prompt = prompt.strip()

        if not prompt:
            raise ValueError("Prompt cannot be empty")

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }

        request = urllib.request.Request(
            url=f"{self.base_url}/api/generate",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                result = json.loads(response.read().decode("utf-8"))
        except urllib.error.URLError as exc:
            raise RuntimeError(
                "Unable to connect to Ollama. Ensure Ollama is running."
            ) from exc

        answer = result.get("response", "").strip()

        if not answer:
            raise RuntimeError("Ollama returned an empty response")

        return answer