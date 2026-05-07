import os
from dotenv import load_dotenv
import requests

load_dotenv()

class OpenRouterClient:
    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise RuntimeError(
                "OPENROUTER_API_KEY is not set. "
                "Set it in your environment or in a .env file."
            )
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.default_headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "http://localhost:5000",
            "Content-Type": "application/json",
        }

    def generate(self, prompt: str, model: str ="meta-llama/llama-3.3-70b-instruct") -> str:
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
        }

        response = requests.post(self.base_url, headers=self.default_headers, json=payload)
        if response.status_code != 200:
            print(f"DEBUG: Status {response.status_code}")
            print(f"DEBUG: Response Body -> {response.text}")
            response.raise_for_status()
            
        return response.json()["choices"][0]["message"]["content"]


