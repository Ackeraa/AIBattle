from skills.skill_base import SkillBase


# skill 1
class SkillStun(SkillBase):
    def __init__(self, cost, time, delay=0, range=10):
        super().__init__("Stun", "Stun the enemy", cost, range)
        self.delay = delay
        self.time = time
        self.used_at = -1

    def use(self, player, opp, ticks):
        self.used_at = ticks
        self.player = player
        self.opp = opp

    def update(self, ticks):
        if self.used_at == -1:
            return

        if self.used_at + self.delay >= ticks:
            if self.calc_dis(self.player, self.opp) <= self.range:
                self.opp.stunned = True
                self.player.attr.hp -= self.cost

        if self.used_at + self.delay + self.time <= ticks:
            self.opp.stunned = False
            self.used_at = -1

    def calc_dis(self, player, opp):
        return abs(player.body[0] - opp.body[0]) + abs(player.body[1] - opp.body[1])
