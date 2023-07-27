from skills.skill_base import SkillBase


# skill 0
class SkillAttack(SkillBase):
    def __init__(self, cost, damage, delay=0, range=1):
        super().__init__("Attack", "Attack the enemy", cost, range)
        self.damage = damage
        self.delay = delay
        self.used_at = 0

    def use(self, ticks, player, opp):
        self.player = player
        self.opp = opp
        self.used_at = ticks
        player.attr.hp -= self.cost

    def update(self, ticks):
        if self.used_at + self.delay >= ticks:
            if self.calc_dis(self.player, self.opp) <= self.range:
                self.opp.attr.hp -= self.damage
                self.used_at = 0

    def calc_dis(self, player, opp):
        return abs(player.body[0] - opp.body[0]) + abs(player.body[1] - opp.body[1])
