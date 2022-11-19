from abc import ABC, abstractmethod


class AbstractProgram(ABC):
    @abstractmethod
    def run(self):
        pass
