import pygame as pg
import random
import time
import os
import numpy as np
from nn import Net
from player import Player
from players_attr import get_player_attr
from settings import *


class Game:
    def __init__(
        self,
        player1_genes,
        player2_genes,
        show=False,
        rows=ROWS,
        cols=COLS,
    ):
        self.Y = rows
        self.X = cols
        self.show = show

        self.ticks = 0

        # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        board = [[x, y] for x in range(self.X) for y in range(self.Y)]

        player1 = Player(
            body=random.choice(board),
            attr=get_player_attr(0),
            nn=Net(weights=player1_genes.copy()),
            board_x=self.X,
            board_y=self.Y,
        )
        player2 = Player(
            body=random.choice(board),
            attr=get_player_attr(1),
            nn=Net(weights=player2_genes.copy()),
            board_x=self.X,
            board_y=self.Y,
        )
        player1.opp = player2
        player2.opp = player1
        self.players = [player1, player2]

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

            for player in self.players:
                player.get_action()

            # print(
            #     ACTIONS[self.players[0].actions[-1]],
            #     "  ",
            #     ACTIONS[self.players[1].actions[-1]],
            # )

            for player in self.players:
                player.react(self.ticks)

            self._update()

            if self._is_over():
                if self.show:
                    self._draw()
                return (
                    self.players[0].attr.hp,
                    self.players[1].attr.hp,
                    self.ticks,
                )

    def _is_over(self):
        """Check if the game is over."""
        # If one player's hp is less than 0, the game is over.
        for player in self.players:
            if player.attr.hp <= 0:
                return True

        # If player1 away from player2 of more than MAX_AWAY_DIS, the game is over.
        if (
            abs(self.players[0].body[0] - self.players[1].body[0])
            + abs(self.players[0].body[1] - self.players[1].body[1])
            > MAX_AWAY_DIS
        ):
            self.players[0].attr.hp = 0

            return True

        # If ticks is more than MAX_TICKS, the game is over.
        if self.ticks > MAX_TICKS:
            # TODO: could let player1 die
            return True

    def _update(self):
        for player in self.players:
            player.update(self.ticks)

        self.ticks += 1

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

        # Draw player's hp text
        for i, player in enumerate(self.players):
            hp = str(player.attr.hp)
            text = f"HP{i+1}:  {str(player.attr.hp)}"
            text_len = len(text) // 2 * 10
            text = pg.font.SysFont(FONT_NAME, 20).render(text, True, WHITE)
            text_rect = text.get_rect()
            text_rect.center = (
                MARGIN_SIZE
                + text_len
                + i * (self.width - 2 * MARGIN_SIZE - 2 * text_len),
                MARGIN_SIZE // 2,
            )
            self.screen.blit(text, text_rect)

        # Draw player's action text
        for i, player in enumerate(self.players):
            text = f"P{i+1}:  {str(ACTIONS[player.actions[-1]])}"
            text_len = len(text) // 2 * 10
            text = pg.font.SysFont(FONT_NAME, 16).render(text, True, WHITE)
            text_rect = text.get_rect()
            text_rect.center = (
                MARGIN_SIZE // 4
                + text_len
                + i * (self.width - MARGIN_SIZE * 2 - text_len),
                self.height - MARGIN_SIZE // 2,
            )
            self.screen.blit(text, text_rect)

        # Draw player
        for player in self.players:
            pg.draw.rect(
                self.screen,
                player.attr.color,
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
        time.sleep(1)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                pg.quit()
                quit()


def best_vs_opp(generation):
    """Use the saved Neural Network model play the game.
    Args:
        generation: the generation of the saved model.
    """
    for filename in os.listdir(os.path.join("genes", str(generation))):
        if filename.startswith("opp"):
            opp_genes_pth = os.path.join("genes", str(generation), filename)
            with open(opp_genes_pth, "rb") as f:
                opp_genes = np.load(f)
        elif filename.startswith("best"):
            best_genes_pth = os.path.join("genes", str(generation), filename)
            with open(best_genes_pth, "rb") as f:
                best_genes = np.load(f)

    game = Game(best_genes, opp_genes, show=True)
    game.play()


def all_vs_opp(generation):
    """Use the saved population's genes play the game.
    Args:
        n: the size of the population.
    """
    genes_list = []

    for filename in os.listdir(os.path.join("genes", str(generation))):
        if filename.startswith("opp"):
            opp_genes_pth = os.path.join("genes", str(generation), filename)
            with open(opp_genes_pth, "rb") as f:
                opp_genes = np.load(f)
        elif filename.startswith("best"):
            pass
        else:
            genes_pth = os.path.join("genes", str(generation), filename)
            with open(genes_pth, "rb") as f:
                genes = np.load(f)
                genes_list.append(genes)

    for genes in genes_list:
        game = Game(genes, opp_genes, show=True)
        game.play()


if __name__ == "__main__":
    best_vs_opp(6083)
