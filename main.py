from math import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from sys import *
import numpy as np

from constants import *
from objectCreation import *
from playerState import *
from texture import *
from gamePhysics import *


x = 0
y = 0
time = 0
shot = False

mouse_x1 = 0
mouse_y1 = 0
mouse_x2 = 1
mouse_y2 = 1

delta_x = 0
delta_y = 0
theta = 0
force = 0
###################################
def drawHealthBar(player):
    if player == "CAT":
        bar = Rectangle((WINDOW_WIDTH // 15) + (WINDOW_WIDTH // 3), WINDOW_WIDTH // 15,\
                        WINDOW_HEIGHT - 15, WINDOW_HEIGHT - 15 - 25)
        glLineWidth(5)
        bar.draw_rect([0, 0, 0, 1], GL_LINE_LOOP)
        bar.right = bar.left + (WINDOW_WIDTH // 3) * CAT_RESULT / WINNING_CONDITION 
        bar.draw_rect([1, 0, 0, 1], GL_QUADS)
    else:
        bar = Rectangle(WINDOW_WIDTH - WINDOW_WIDTH // 15, \
                        WINDOW_WIDTH - WINDOW_WIDTH // 15 -  WINDOW_WIDTH // 3, WINDOW_HEIGHT - 15,\
                        WINDOW_HEIGHT - 15 - 25)

        glLineWidth(5)
        bar.draw_rect([0, 0, 0, 1], GL_LINE_LOOP)
        bar.left = bar.right - (WINDOW_WIDTH // 3) * DOG_RESULT / WINNING_CONDITION 
        bar.draw_rect([1, 0, 0, 1], GL_QUADS)


###################################
def dynamics():
    global shot, force, mouse_x1, mouse_y1, mouse_x2, mouse_y2, delta_x, delta_y, theta
    delta_x = mouse_x1 - mouse_x2
    delta_y = mouse_y1 - mouse_y2
    force = sqrt(pow(delta_x, 2) + pow(delta_y, 2))
    if delta_x > 0 and delta_y > 0:
        theta = 360 - degrees(atan(delta_y / delta_x))
    elif delta_x < 0 < delta_y:
        theta = 180 + degrees(atan(delta_y / -delta_x))
    elif delta_x < 0 and delta_y < 0:
        theta = 180 - degrees(atan(-delta_y / -delta_x))
    elif delta_x > 0 > delta_y:
        theta = degrees(atan(-delta_y / delta_x))
    else:
        shot = False
    theta -= 180

def check_collision(ball):
    global CAT, DOG, CAT_RESULT, DOG_RESULT, shot, x, y, theta, force, time, CURRENT_TURN
    # Dog Points
    if CURRENT_TURN == "DOG" and ball.bottom <= CAT.top:
        if CAT.right >= ball.left >= CAT.left:
            CAT_RESULT -= 1
            shot = False
            ball.start("CAT")
            CURRENT_TURN = "CAT"
    # Cat Points
    if CURRENT_TURN == "CAT" and ball.bottom <= DOG.top:
        if DOG.right >= ball.right >= DOG.left:
            DOG_RESULT -= 1
            shot = False
            ball.start("DOG")
            CURRENT_TURN = "DOG"
#############################################

def mouseButton(key, state, xc, yc):
    global mouse_x1, mouse_y1, mouse_x2, mouse_y2, theta, delta_x, delta_y, force, \
    shot, x, y, time, CURRENT_TURN, CAT_RESULT, DOG_RESULT, DOG_STATE, CAT_STATE
    
    if key == GLUT_LEFT_BUTTON and state == GLUT_DOWN:  
        mouse_x1 = xc
        mouse_y1 = yc
    elif key == GLUT_LEFT_BUTTON and state == GLUT_UP:
        mouse_x2 = xc
        mouse_y2 = yc
        if not shot:
            shot = True
            dynamics()
            x = ball.X
            y = ball.Y
            time = 0


def display():
    global mouse_x1, mouse_y1, mouse_x2, mouse_y2, theta, delta_x, delta_y, force, \
    CAT_RESULT, DOG_RESULT, x, y, time, shot, LOSE, CURRENT_TURN
    glClear(GL_COLOR_BUFFER_BIT)
    game()
    glutSwapBuffers()

def game_timer(v):
    display()
    glutTimerFunc(Time, game_timer, v)

def init():
    glClearColor(0, 0, 0, 1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, 0, 1)  
    glMatrixMode(GL_MODELVIEW)

def game():
    global mouse_x1, mouse_y1, mouse_x2, mouse_y2, theta, delta_x, delta_y, force, \
    CAT_RESULT, DOG_RESULT, x, y, time, shot, ROTATION_ANGLE, DOG_STATE, CAT_STATE, LOSE, ball, \
    middle_wall, CURRENT_TURN, MAIN, END, START, WINNING_CONDITION
    
    if CURRENT_TURN == "DOG" and not shot:
        DOG_STATE = "READY"
        CAT_STATE = "IDLE"
    elif CURRENT_TURN == "CAT" and not shot:
        CAT_STATE = "READY"
        DOG_STATE = "IDLE"

    # Drawing the objects
    background = Rectangle(WINDOW_WIDTH, 0, WINDOW_HEIGHT, 0)
    background.draw_rectangle_texture(0)
    if shot:
        glPushMatrix()
        glTranslate(ball.X, ball.Y, 0)  
        glRotate(ROTATION_ANGLE, 0, 0, 1)
        ROTATION_ANGLE += 10
        glTranslate(-ball.X, -ball.Y, 0)  
        ball.draw_rectangle_texture(get_ball_texture(CURRENT_TURN))  
        glPopMatrix()
    DOG.draw_rectangle_texture(get_dog_texture(DOG_STATE))
    CAT.draw_rectangle_texture(get_cat_texture(CAT_STATE))
    middle_wall.draw_rectangle_texture(9)
    check_collision(ball)
    drawHealthBar("CAT")
    drawHealthBar("DOG")
    if shot:
        if CURRENT_TURN == "DOG":  
            DOG_STATE = "THROW"
        else:
            CAT_STATE = "THROW"        
        if ball.bottom > 0 and not wall_collision(middle_wall, ball) and \
            ball.left > 0 and ball.right < WINDOW_WIDTH:  
            glLoadIdentity()
            time += 0.05  
            path = object_path(x, y, force, radians(theta), time)              
            for i in np.arange(theta, theta + 360, 1):
                glPushMatrix()
                glRotate(i, 1, 0, 0)
                ball.draw_rectangle_texture(get_ball_texture(CURRENT_TURN))
                glPopMatrix()
            ball.left = path[0] - BALL_SIZE // 2
            ball.right = path[0] + BALL_SIZE // 2
            ball.top = path[1] + BALL_SIZE // 2
            ball.bottom = path[1] - BALL_SIZE // 2
            ball.refresh()
        else:  
            shot = False
            if CURRENT_TURN == "DOG":
                ball.start("CAT")
                CURRENT_TURN = "CAT"
            else:
                ball.start("DOG")
                CURRENT_TURN = "DOG"

if __name__ == "__main__":
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(0, 0)
    glutCreateWindow("CAT Vs DOG")
    glutDisplayFunc(display)
    glutTimerFunc(Time, game_timer, 1)
    glutMouseFunc(mouseButton)
    init()
    Texture_init()
    glutMainLoop()

