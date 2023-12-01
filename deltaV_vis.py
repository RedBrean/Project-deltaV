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
    """Рисовабельные предметы"""
    def __init__(self, spriteFileName = None, x = None, y = None):
        #можно читать из файла проекта спрайт
        if(x!=None and y!=None):
            self.x = x
            self.y = y
    def GetSurface(self) -> pg.Surface:
        #Долно скидывать полотно которое нужно вывести на экран
        pass
    def GetRect(self, Camera) -> pg.Rect:
        #должно понимать где оно должно рисовать
        pass
        
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
    def __init__(self,screen,drawble_objects):
        self.screen=screen
        self.drawble_objects=drawble_objects
    def draw(self,cam):
        #Проходит по всем объектам в списке этого же класса и рисует их
        self.screen.fill(BLACK)
        for i in self.drawble_objects:
            rel_x,rel_y=i.abs_x-cam.x,i.abs_y-cam.y
            if i.type=="circle":
                pg.draw.circle(self.screen, i.color, (rel_x, rel_y), 50*i.scale)
            
            
