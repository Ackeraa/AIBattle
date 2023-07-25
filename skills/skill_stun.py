from skill_base import SkillBase


class SkillStun(SkillBase):
    def __init__(self, cost, delay=0, range=1):
        super().__init__("Stun", "Stun the enemy", cost, range)
        self.delay = delay
