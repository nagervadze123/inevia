from abc import ABC, abstractmethod


class AIProvider(ABC):
    @abstractmethod
    def complete_json(self, system_prompt: str, user_prompt: str) -> dict:
        raise NotImplementedError


class MockAIProvider(AIProvider):
    def complete_json(self, system_prompt: str, user_prompt: str) -> dict:
        return {"system_prompt": "suppressed", "user_prompt": "suppressed"}
