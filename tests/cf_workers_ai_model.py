import json

import requests
from deepeval.models import DeepEvalBaseLLM
from pydantic import BaseModel


class CloudflareWorkersAI(DeepEvalBaseLLM):
    """Custom DeepEval LLM evaluator using Cloudflare Workers AI."""

    def __init__(self, account_id: str, api_token: str, model: str = "@cf/meta/llama-3.1-8b-instruct"):
        self.account_id = account_id
        self.api_token = api_token
        self.model_name = model
        self.api_url = (
            f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/{model}"
        )

    def load_model(self):
        return self.model_name

    def generate(self, prompt: str, schema: BaseModel | None = None) -> str | BaseModel:
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }
        payload = {
            "messages": [
                {"role": "user", "content": prompt},
            ],
        }

        response = requests.post(self.api_url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()
        output = result["result"]["response"]

        if schema is not None:
            try:
                parsed = json.loads(output)
                return schema(**parsed)
            except (json.JSONDecodeError, Exception):
                cleaned = output.strip()
                if "```json" in cleaned:
                    cleaned = cleaned.split("```json")[1].split("```")[0].strip()
                elif "```" in cleaned:
                    cleaned = cleaned.split("```")[1].split("```")[0].strip()
                parsed = json.loads(cleaned)
                return schema(**parsed)

        return output

    async def a_generate(self, prompt: str, schema: BaseModel | None = None) -> str | BaseModel:
        return self.generate(prompt, schema)

    def get_model_name(self) -> str:
        return self.model_name
