from math import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from sys import *
import pygame

from constants import *


def get_dog_texture(state):
    if state == "IDLE":
        return 1
    elif state == "READY":
        return 2
    elif state == "THROW":
        return 3

def get_cat_texture(state):
    if state == "IDLE":
        return 5
    elif state == "READY":
        return 6
    elif state == "THROW":
        return 7

def get_ball_texture(CURRENT_TURN):
    if CURRENT_TURN == "DOG":
        return 4
    else:
        return 8


