from typing import Dict, Any, Optional
from .settings import settings

class LLMClient:
    def __init__(self) -> None:
        self.provider = settings.llm_provider
        self.model = settings.openai_model
        self.api_key = settings.openai_api_key

    def complete(self, prompt: str, system: Optional[str] = None) -> str:
        # Offline fallback
        if self.provider == 'offline' or not self.api_key:
            return self._offline(prompt, system)

        if self.provider == 'openai':
            try:
                # Lazy import to keep dependency optional
                from openai import OpenAI
                client = OpenAI(api_key=self.api_key)
                resp = client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {'role': 'system', 'content': system or 'You are a helpful healthcare assistant. No diagnosis.'},
                        {'role': 'user', 'content': prompt},
                    ],
                    temperature=0.2,
                )
                return resp.choices[0].message.content
            except Exception as e:
                return f'[LLM error: {e}] Using offline fallback.\n' + self._offline(prompt, system)

        # Default fallback
        return self._offline(prompt, system)

    def _offline(self, prompt: str, system: Optional[str]) -> str:
        guidance = (
            'I am not a doctor, but here is general guidance based on your input. '
            'If symptoms are severe or worsening, seek medical attention immediately.'
        )
        return f"""{guidance}

Key points you mentioned (sampled):
- {prompt[:200]}...
"""
