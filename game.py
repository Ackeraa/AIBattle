import pygame as pg
import random
from player import Player, PlayerAttr
from settings import *


class Game:

    def __init__(self, player1_attr, player2_attr, show=False, rows=ROWS, cols=COLS):
        self.Y = rows
        self.X = cols
        self.show = show

        self.players = []
        board = [(x, y) for x in range(self.X) for y in range(self.Y)]

        self.players.append(Player(body=random.choice(board),
                                   attr=player1_attr, policy=None, board_x=self.X, board_y=self.Y))

        self.players.append(Player(body=random.choice(board),
                                   attr=player2_attr, policy=None, board_x=self.X, board_y=self.Y))

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
                player.move()

    def _draw(self):
        self.screen.fill(BGCOLOR)

        # Draw grid
        for i in range(0, self.X + 1):
            pg.draw.line(self.screen, LINE_COLOR, (i * GRID_SIZE + MARGIN_SIZE, MARGIN_SIZE),
                         (i * GRID_SIZE + MARGIN_SIZE, self.height - MARGIN_SIZE), 1)
        for i in range(0, self.Y + 1):
            pg.draw.line(self.screen, LINE_COLOR, (MARGIN_SIZE, i * GRID_SIZE + MARGIN_SIZE),
                         (self.width - MARGIN_SIZE, i * GRID_SIZE + MARGIN_SIZE), 1)

        # Draw player
        for player in self.players:
            pg.draw.rect(self.screen, player.color,
                         (player.body[0] * GRID_SIZE + MARGIN_SIZE,
                          player.body[1] * GRID_SIZE + MARGIN_SIZE,
                          GRID_SIZE, GRID_SIZE))

        pg.display.flip()

    def _event(self):
        """Get event from user interaction"""
        self.clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                pg.quit()
                quit()


if __name__ == "__main__":
    basic_player_attr = PlayerAttr(hp=100, atk=10, spd=10, rng=1)
    game = Game(player1_attr=basic_player_attr,
                player2_attr=basic_player_attr, show=True)
    game.play()
