from skill_base import SkillBase


class SkillAttack(SkillBase):
    def __init__(self, cost, damage, delay=1, range=1):
        super().__init__("Attack", "Attack the enemy", cost, range)
        self.damage = damage
        self.delay = delay

    def use(self, player, opp):
        if player.attr.energy < self.cost:
            return False
        if self.delay > 0:
            self.delay -= 1
            return False
        player.attr.energy -= self.cost
        opp.attr.hp -= self.damage
        return True
