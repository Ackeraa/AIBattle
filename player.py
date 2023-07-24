from settings import *
import time
import random


class PlayerAttr:
    def __init__(self, hp, atk, spd, rng):
        self.hp = hp
        self.atk = atk
        self.spd = spd
        self.rng = rng


class Player:
    def __init__(self, body, attr, policy, board_x, board_y):
        self.body = body
        self.attr = attr
        self.policy = policy
        self.board_x = board_x
        self.board_y = board_y
        self.color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )

    def move(self):
        time.sleep(2)
        move_dir = random.choice(DIRECTIONS)
        self.body = (self.body[0] + move_dir[0], self.body[1] + move_dir[1])

    def attack(self):
        pass

    def defend(self):
        pass

    def get_state(self):
        pass
