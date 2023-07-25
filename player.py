from settings import *
import numpy as np
from nn import Net
import time
import random


class PlayerAttr:
    def __init__(self, hp, spd, skills):
        self.hp = hp
        self.spd = spd
        self.skills = skills


class Player:
    def __init__(self, body, attr, genes):
        self.body = body
        self.attr = attr
        self.nn = Net(N_INPUT, N_HIDDEN1, N_HIDDEN2, N_OUTPUT, genes.copy())
        self.actions = []
        self.color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )

    def react(self, state):
        action = self.nn.predict(state)
        if len(self.actions) > HISTORY_LEN:
            self.actions.pop(0)
        self.actions.append(action)

    def use_skill(self, skill, opp):
        if self.attr.skills[skill] is None:
            return

        self.attr.skills[skill].use(self, opp)
