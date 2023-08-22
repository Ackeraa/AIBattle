from skills.skill_attack import SkillAttack
from skills.skill_stun import SkillStun

TITTLE = "AI Battle"
FONT_NAME = "arial"
FPS = 60
ROWS = 6
COLS = 6
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
PLAYER1_HP = 100
PLAYER2_HP = 100
SKILLS = [
    SkillAttack(10, 10, 0, 1),
    SkillStun(10, 3, 0, 10),
]

SKILL_NUMS = len(SKILLS)
ACTION_NUMS = SKILL_NUMS + 3
HISTORY_LEN = 3
MAX_AWAY_DIS = 10  # if dis larger than this, the player1 will die, game over

MAX_TICKS = 100
ACTIONS = ["Do nothing", "Move towards", "Move away"]
for skill in SKILLS:
    ACTIONS.append(f"Use {skill.name}")

# AI settings
N_INPUT = ACTION_NUMS + 3
N_HIDDEN1 = 30
N_HIDDEN2 = 20
N_OUTPUT = ACTION_NUMS
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
MUTATE_RATE = 0.12

INIT_UPDATE_GAP = 1000  # initial gap between two updates of the opponent genes
UPDATE_RATE = 1.3  # update gap will be multiplied by this after each update

SAVE_GAP = 50  # save the all individual every SAVE_GAP generations
