from abc import ABC, abstractmethod


class SkillBase(ABC):
    def __init__(self, name, description, cost, range):
        self.name = name
        self.description = description
        self.cost = cost
        self.range = range

    @abstractmethod
    def use(self, player, opp):
        pass

    @abstractmethod
    def update(self, clock):
        pass
