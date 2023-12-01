"""Здесь все что касается нарисовать что-то на экране"""
import pygame as pg
from deltaV_settings import *
import pyautogui



class Drawable(object):
    """Рисовабельные предметы"""
    def __init__(self, spriteFileName = None, x = None, y = None):
        #можно читать из файла проекта спрайт
        if(x!=None and y!=None):
            self.x = x
            self.y = y
    def GetSurface(self, camera) -> pg.Surface:
        #Долно скидывать полотно которое нужно вывести на экран
        pass
    def GetRect(self, camera) -> pg.Rect:
        #должно понимать где оно должно рисовать
        pass
        
class Camera():
    def __init__(self,x=0,y=0):
        self.x=x
        self.y=y
        self.scale = 1
    def set_up_defoult(self, game_objects : list[Drawable]):
        xs = []
        ys = []
        for game_object in game_objects:
            xs.append(game_object.x)
            ys.append(game_object.y)

        maxX = max(xs)
        maxY = max(ys)
        minX = min(xs)
        minY = min(ys)

        self.x = (maxX+minX)/2
        self.y = (maxY+minY)/2

        self.scale = min()

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
    def __init__(self,screen : pg.Surface, drawble_objects : list[Drawable]):
        self.screen=screen
        self.drawble_objects=drawble_objects
    def draw(self, camera):
        #Проходит по всем объектам в списке этого же класса и рисует их
        self.screen.fill(BLACK)
        for cDrawebleObject in self.drawble_objects:
            self.screen.blit(cDrawebleObject.GetSurface(camera), cDrawebleObject.GetRect(camera))
            
