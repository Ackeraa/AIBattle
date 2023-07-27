from player import PlayerAttr
from settings import *


def choose_skills(skill_ids):
    skills = {}
    for i in skill_ids:
        skills[i] = SKILLS[i]
    return skills


player1_attr = PlayerAttr(hp=100, color=RED, skills=choose_skills([0]))
player2_attr = PlayerAttr(hp=100, color=BLUE, skills=choose_skills([0]))
