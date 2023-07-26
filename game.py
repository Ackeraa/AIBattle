import pygame as pg
import random
import numpy as np
import os
from player import Player, PlayerAttr
from settings import *


class Game:
    def __init__(
        self,
        player1_attr,
        player2_attr,
        player1_genes,
        player2_genes,
        show=False,
        rows=ROWS,
        cols=COLS,
    ):
        self.Y = rows
        self.X = cols
        self.show = show

        self.clock = 0

        self.players = []
        board = [(x, y) for x in range(self.X) for y in range(self.Y)]

        self.players.append(
            Player(
                body=random.choice(board),
                attr=player1_attr,
                genes=player1_genes,
            )
        )

        self.players.append(
            Player(
                body=random.choice(board),
                attr=player2_attr,
                genes=player2_genes,
            )
        )

        if self.show:
            pg.init()
            self.width = cols * GRID_SIZE + 2 * MARGIN_SIZE
            self.height = rows * GRID_SIZE + 2 * MARGIN_SIZE

            pg.display.set_caption(TITTLE)
            self.screen = pg.display.set_mode((self.width, self.height))
            self.clock = pg.time.Clock()
            self.font_name = pg.font.match_font(FONT_NAME)

    def play(self):
        while True:
            if self.show:
                self._event()
                self._draw()

            for i, player in enumerate(self.players):
                state = self.get_state(i)
                player.react(state)

            for i, player in enumerate(self.players):
                self._react(i)

            self._update()

    def _react(self, who):
        """
        0: move towards opp
        1: move away from opp
        2: do nothing
        else: use skill
        """
        player = self.players[who]
        opp = self.players[1 - who]

        action = player.actions[-1]

        if action == 0:
            self._move_towards(player, opp)
        elif action == 1:
            self._move_away(player, opp)
        elif action == 2:
            pass
        else:
            player.use_skill(action - 2, opp)

    def _move_towards(self, player, opp):
        player_x, player_y = player.body
        opp_x, opp_y = opp.body

        # move horizontally first
        if player_x != opp_x:
            player.body[0] += 1 if player_x < opp_x else -1
        # move vertically then
        elif player_y != opp_y:
            player.body[1] += 1 if player_y < opp_y else -1

    def _move_away(self, player, opp):
        player_x, player_y = player.body
        opp_x, opp_y = opp.body

        # move horizontally first
        if player_x != opp_x:
            if 0 < player_x < self.X - 1:
                player.body[0] -= 1 if player_x < opp_x else -1
        # move vertically then
        elif player_y != opp_y:
            if 0 < player_y < self.Y - 1:
                player.body[1] -= 1 if player_y < opp_y else -1

    def _get_state(self, who):
        """
        player's:
          hp 1
        opp's:
          hp 1
          last action ACTION_NUMS
        distance:
          to opp 1
        """
        player = self.players[who]
        opp = self.players[1 - who]
        state = []

        # player's hp
        state.append(1.0 / player.attr.hp)

        # opp's hp
        state.append(1.0 / opp.attr.hp)

        # opp's last action
        actions = [0] * ACTION_NUMS
        actions[opp.actions[-1]] = 1
        state.extend(actions)

        # distance to opp
        state.append(
            1.0
            / (abs(player.body[0] - opp.body[0]) + abs(player.body[1] - opp.body[1]))
        )

        return state

    def _update(self):
        self.clock += 1
        for player in self.players:
            player.update(self.clock)

    def _draw(self):
        self.screen.fill(BGCOLOR)

        # Draw grid
        for i in range(0, self.X + 1):
            pg.draw.line(
                self.screen,
                LINE_COLOR,
                (i * GRID_SIZE + MARGIN_SIZE, MARGIN_SIZE),
                (i * GRID_SIZE + MARGIN_SIZE, self.height - MARGIN_SIZE),
                1,
            )
        for i in range(0, self.Y + 1):
            pg.draw.line(
                self.screen,
                LINE_COLOR,
                (MARGIN_SIZE, i * GRID_SIZE + MARGIN_SIZE),
                (self.width - MARGIN_SIZE, i * GRID_SIZE + MARGIN_SIZE),
                1,
            )

        # Draw player
        for player in self.players:
            pg.draw.rect(
                self.screen,
                player.color,
                (
                    player.body[0] * GRID_SIZE + MARGIN_SIZE,
                    player.body[1] * GRID_SIZE + MARGIN_SIZE,
                    GRID_SIZE,
                    GRID_SIZE,
                ),
            )

        pg.display.flip()

    def _event(self):
        """Get event from user interaction"""
        self.clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                pg.quit()
                quit()


def play_best(score):
    """Use the saved Neural Network model play the game.
    Args:
        score: Specify which individual's genes to load, also indicates the highest score it can get.
    """
    genes_pth = os.path.join("genes", "best", str(score))
    with open(genes_pth, "r") as f:
        genes = np.array(list(map(float, f.read().split())))


def play_all(n=P_SIZE):
    """Use the saved population's genes play the game.
    Args:
        n: the size of the population.
    """
    genes_list = []
    for i in range(n):
        genes_pth = os.path.join("genes", "all", str(i))
        with open(genes_pth, "r") as f:
            genes = np.array(list(map(float, f.read().split())))
        genes_list.append(genes)


if __name__ == "__main__":
    basic_player_attr = PlayerAttr(hp=100, atk=10, spd=10, rng=1)
    game = Game(
        player1_attr=basic_player_attr, player2_attr=basic_player_attr, show=True
    )
    game.play()
