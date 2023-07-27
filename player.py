from settings import *
from nn import Net
import random


class PlayerAttr:
    def __init__(self, hp, color, skills):
        self.hp = hp
        self.color = color
        self.skills = skills


class Player:
    def __init__(self, body, attr, genes, board_x, board_y, opp=None):
        self.body = body
        self.attr = attr
        self.nn = Net(N_INPUT, N_HIDDEN1, N_HIDDEN2, N_OUTPUT, genes.copy())
        self.actions = [0]
        self.opp = opp
        self.board_x = board_x
        self.board_y = board_y

    def get_action(self):
        state = self._get_state()
        action = self.nn.predict(state)
        if len(self.actions) > HISTORY_LEN:
            self.actions.pop(0)
        self.actions.append(action)

    def react(self):
        """
        0: do nothing
        1: move towards opp
        2: move away from opp
        else: use skill
        """

        action = self.actions[-1]
        if action == 0:
            pass
        elif action == 1:
            self._move_towards()
        elif action == 2:
            self._move_away()
        else:
            self._use_skill(action - 2)

    def _get_state(self):
        """
        player's:
          hp 1
        opp's:
          hp 1
          last action ACTION_NUMS
        distance:
          to opp 1
        """
        state = []

        # player's hp
        state.append(1.0 / max(1, self.attr.hp))

        # opp's hp
        state.append(1.0 / max(1, self.opp.attr.hp))

        # opp's last action
        actions = [0] * ACTION_NUMS
        actions[self.actions[-1]] = 1
        state.extend(actions)

        # distance to opp
        state.append(
            1.0
            / max(
                1,
                (
                    abs(self.body[0] - self.opp.body[0])
                    + abs(self.body[1] - self.opp.body[1])
                ),
            )
        )

        return state

    def _move_towards(self):
        player_x, player_y = self.body
        opp_x, opp_y = self.opp.body

        # move horizontally first
        if player_x != opp_x:
            self.body[0] += 1 if player_x < opp_x else -1
        # move vertically then
        elif player_y != opp_y:
            self.body[1] += 1 if player_y < opp_y else -1

    def _move_away(self):
        player_x, player_y = self.body
        opp_x, opp_y = self.opp.body

        # move horizontally first
        if player_x != opp_x:
            if 0 < player_x < self.board_x - 1:
                self.body[0] -= 1 if player_x < opp_x else -1
        # move vertically then
        elif player_y != opp_y:
            if 0 < player_y < self.board_y - 1:
                self.body[1] -= 1 if player_y < opp_y else -1
        else:
            # move left first
            if player_x > 0:
                self.body[0] -= 1
            # move right then
            elif player_x < self.board_x - 1:
                self.body[0] += 1
            # move up then
            elif player_y > 0:
                self.body[1] -= 1
            # move down then
            elif player_y < self.board_y - 1:
                self.body[1] += 1

    def _use_skill(self, skill):
        if skill not in self.attr.skills:
            return

        self.attr.skills[skill].use(self, self.opp)

    def update(self, ticks):
        for skill in self.attr.skills.values():
            skill.update(ticks)
