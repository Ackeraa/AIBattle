from player import PlayerAttr, Player
from skills.skill_attack import SkillAttack

TITTLE = "AI Battle"
FONT_NAME = "arial"
FPS = 60
ROWS = 10
COLS = 10
GRID_SIZE = 40
MARGIN_SIZE = 50

DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = BLACK
LINE_COLOR = WHITE

INF = 100000000

# Player settings
SKILL_NUMS = 1
ACTION_NUMS = SKILL_NUMS + 2
HISTORY_LEN = 3

SKILLS = [
    SkillAttack(10, 10, 0, 1),
]


def CHOOSE_SKILLS(skill_ids):
    global SKILLS
    skills = {}
    for i in skill_ids:
        skills[i] = SKILLS[i]
    return skills


PLAYER1_ATTR = PlayerAttr(hp=100, skills=CHOOSE_SKILLS([0]))
PLAYER2_ATTR = PlayerAttr(hp=100, skills=CHOOSE_SKILLS([0]))

# AI settings
N_INPUT = 6
N_HIDDEN1 = 20
N_HIDDEN2 = 12
N_OUTPUT = ACTION_NUMS + 3
GENES_LEN = (
    N_INPUT * N_HIDDEN1
    + N_HIDDEN1 * N_HIDDEN2
    + N_HIDDEN2 * N_OUTPUT
    + N_HIDDEN1
    + N_HIDDEN2
    + N_OUTPUT
)
P_SIZE = 100
C_SIZE = 400
MUTATE_RATE = 0.1
UPDATE_GENE_STEP = 1000
