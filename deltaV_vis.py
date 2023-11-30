"""Здесь все что касается нарисовать что-то на экране"""
import pygame as pg
import pyautogui

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D

class Drawable(object):
    list_of_em=[]
    """Рисовабельные предметы"""
    def __init__(self,type,abs_x,abs_y,scale,color):
        self.type=type
        self.abs_x=abs_x
        self.abs_y=abs_y
        self.scale=scale
        self.color=color
        Drawable.list_of_em.append(self)
class Camera():
    def __init__(self,x=0,y=0):
        self.x=x
        self.y=y
    def move(self,event):
        if event.type==pg.KEYDOWN:
            if event.key==pg.K_UP:
                self.y-=10
            elif event.key==pg.K_DOWN:
                self.y+=10
            elif event.key==pg.K_RIGHT:
                self.x+=10
            elif event.key==pg.K_LEFT:
                self.x-=10

        

class ScreenDrawer():
    """Класс отвечающий за вывод на экран"""
    def __init__(self,screen):
        self.screen=screen
    def draw(self,cam):
        self.screen.fill(BLACK)
        for i in Drawable.list_of_em:
            rel_x,rel_y=i.abs_x-cam.x,i.abs_y-cam.y
            if i.type=="circle":
                pg.draw.circle(self.screen, i.color, (rel_x, rel_y), 50*i.scale)
            
            
