from math import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from sys import *
import pygame
from os import listdir


texture_order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
object_list = ["/University.jpg", "/DOG_IDEAL.png", "/DOG_READY.png", "/DOG_THROW.png", "/Bone.png",
                 "/CAT_IDEAL.png", "/CAT_READY.png", "/CAT_THROW.png", "/Can.png", "/midWall.png"] 
# object_list = listdir("objects/")

def texture_setup(texture_image_binary, texture_name, width, height):
    glBindTexture(GL_TEXTURE_2D, texture_name) 
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)  
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_image_binary)  
    glBindTexture(GL_TEXTURE_2D, -1)  

def loadTextures():
    glEnable(GL_TEXTURE_2D) 
    texture = []  
    for object in object_list:
        texture.append(pygame.image.load("./objects" + object))      
    # Convert texture to the type needed for textures
    textures = [pygame.image.tostring(image, "RGBA", True) for image in texture] 
    # Generate textures
    glGenTextures(len(texture), texture_order)  
    # Add textures to openGL
    for i in range(len(texture)):
        texture_setup(textures[i], texture_order[i], texture[i].get_width(), texture[i].get_height())

def Texture_init():
    loadTextures()
    glEnable(GL_BLEND)  
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA) 
