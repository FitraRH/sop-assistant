"""Thin client for any OpenAI-compatible chat endpoint (Ollama, Groq, Gemini, OpenAI...)."""
import json
import re

from openai import OpenAI

from .config import Settings


class LLM:
    def __init__(self, s: Settings):
        self.model = s.llm_model
        self.client = OpenAI(base_url=s.llm_base_url, api_key=s.llm_api_key or "none")

    def complete_json(self, system: str, user: str) -> dict:
        args = dict(model=self.model, temperature=0,
                    messages=[{"role": "system", "content": system}, {"role": "user", "content": user}])
        try:
            reply = self.client.chat.completions.create(response_format={"type": "json_object"}, **args)
        except Exception:  # some providers reject response_format
            reply = self.client.chat.completions.create(**args)
        text = reply.choices[0].message.content or ""
        return json.loads(re.search(r"\{.*\}", text, re.S).group(0))  # tolerates ``` fences