from math import *
from OpenGL.GL import *
from OpenGL.GLUT import *

from constants import *


# Object Creation
class Rectangle:
    def __init__(self, right, left, top, bottom):
        self.top = top
        self.bottom = bottom
        self.right = right
        self.left = left
        self.X = (left + right) / 2
        self.Y = (top + bottom) / 2                     

    def draw_rect(self, color, type): 
        glColor(color[0], color[1], color[2], color[3])
        glBegin(type)
        glVertex(self.left, self.bottom, 0)
        glVertex(self.right, self.bottom, 0)
        glVertex(self.right, self.top, 0)
        glVertex(self.left, self.top, 0)
        glEnd()

    def draw_rectangle_texture(self, texture_name):  
        glColor(1,1,1,1)
        glBindTexture(GL_TEXTURE_2D, texture_name)
        glBegin(GL_POLYGON)
        glTexCoord(0, 0)
        glVertex2d(self.left, self.bottom)
        glTexCoord(1, 0)
        glVertex2d(self.right, self.bottom)
        glTexCoord(1, 1)
        glVertex2d(self.right, self.top)
        glTexCoord(0, 1)
        glVertex2d(self.left, self.top)
        glEnd()
        glBindTexture(GL_TEXTURE_2D, -1)


    def refresh(self):   
        self.X = (self.left + self.right) / 2
        self.Y = (self.top + self.bottom) / 2

    def start(self, player):  
        if player == "DOG":
            self.left = DOG.left
            self.bottom = DOG.top - BALL_SIZE//2
            self.right = self.left + BALL_SIZE
            self.top = self.bottom + BALL_SIZE
            self.X = (self.left + self.right) / 2
            self.Y = (self.top + self.bottom) / 2

        else:
            self.left = CAT.right - BALL_SIZE//2
            self.bottom = CAT.top
            self.top = self.bottom - BALL_SIZE
            self.right = self.left + BALL_SIZE
            self.X = (self.left + self.right) / 2
            self.Y = (self.top + self.bottom) / 2


# DOG Object
DOG = Rectangle( WINDOW_WIDTH - WINDOW_WIDTH//6 + PLAYER_WIDTH, 
                WINDOW_WIDTH - WINDOW_WIDTH//6, PLAYER_HEIGHT, 0)

## CAT Object
CAT = Rectangle(PLAYER_WIDTH, 0, PLAYER_HEIGHT, 0)

## Middle Wall Object
middle_wall = Rectangle((50 + WINDOW_WIDTH // 2), (WINDOW_WIDTH // 2 - 50), WINDOW_HEIGHT // 2, 0)

## Ball Object
ball = Rectangle(0, 0, 0, 0)
ball.start(CURRENT_TURN)
