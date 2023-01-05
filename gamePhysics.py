from math import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from sys import *

from constants import *
from playerState import *
from objectCreation import *
from texture import *

def object_path(xc, yc, F, ang, t):
    velx = F * cos(ang)
    vely = F * sin(ang)
    distX = velx * t  
    distY = (vely * t) + ((GRAVITY_ACC * (t) ** 2) / 2) 

    newx = round(distX + xc)
    newy = round(distY + yc)
    return (newx, newy)


def wall_collision(middle_wall, ball):
    if middle_wall.right >= ball.left >= middle_wall.left:
        leftOverlap = True
    else: 
        leftOverlap = False
    if middle_wall.left <= ball.right <= middle_wall.right:
        rightOverlap = True
    else:
        rightOverlap = False
    if ball.bottom <= middle_wall.top:
        verticalCollision = True
    else:
        verticalCollision = False
    return verticalCollision and (leftOverlap or rightOverlap)


