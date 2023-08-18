from player import PlayerAttr
import copy
from settings import *


def choose_skills(skill_ids):
    skills = {}
    for i in skill_ids:
        skills[i] = copy.deepcopy(SKILLS[i])
    return skills


def get_player_attr(i):
    if i == 0:
        return PlayerAttr(hp=PLAYER1_HP, color=BLUE, skills=choose_skills([0]))
    else:
        return PlayerAttr(hp=PLAYER2_HP, color=RED, skills=choose_skills([0]))
