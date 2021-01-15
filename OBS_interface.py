from __future__ import annotations
from abc import ABC, abstractmethod


class Observer(ABC):
    @abstractmethod
    def update(self, recipeId, network_data) -> None:
        pass

class Subject(ABC):
    @abstractmethod
    def attach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def notify(self, recipeId, network_data) -> None:
        pass

