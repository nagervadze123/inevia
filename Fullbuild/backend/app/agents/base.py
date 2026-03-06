from abc import ABC, abstractmethod
from pydantic import BaseModel


class Agent(ABC):
    name: str
    input_schema: type[BaseModel]
    output_schema: type[BaseModel]

    @abstractmethod
    def execute(self, payload: dict) -> BaseModel:
        raise NotImplementedError
