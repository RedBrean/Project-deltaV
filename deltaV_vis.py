"""Здесь все что касается нарисовать что-то на экране"""
import pygame as pg
from deltaV_settings import *

class Drawable(object):
    """Рисовабельные предметы"""
    def __init__(self, spriteFileName = None, x = None, y = None):
        #можно читать из файла проекта спрайт
        self.haveSprite = False
        if(spriteFileName != None):
            self.sprite = pg.image.load(spriteFileName)
            self.haveSprite = True
        if(x!=None and y!=None):
            self.x = x
            self.y = y

    def GetSurface(self, camera) -> pg.Surface:
        #Долно скидывать полотно которое нужно вывести на экран
        #Пока что тут затычка
        width  = 30
        hight = 30
        surf = pg.Surface((width,hight))
        surf.fill(BLACK)
        surf.set_colorkey(BLACK)
        pg.draw.circle(surf, (255, 0, 255), (width/2, hight/2), 10)
        surf = surf.convert_alpha()
        return surf
        
    def GetRect(self, camera) -> pg.Rect:
        #должно понимать где оно должно рисовать
        x = (self.x-camera.x)*camera.scale + WINDOW_WIDTH/2
        y = (self.y-camera.y)*camera.scale + WINDOW_HEIGHT/2
        #FIXME Сейчас прямоугольник всегда 50 на 50
        rect = pg.Rect((0, 0), (50,50))
        rect.center = (x,y)
        return rect
        
class Camera():
    def __init__(self,x=0,y=0):
        self.x=x
        self.y=y
        self.vx=0
        self.vy=0
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
        dX = max((maxX - minX), 1000)
        dY = max((maxY - minY), 1000)
        self.scale = 0.9*min(WINDOW_WIDTH/dX,WINDOW_HEIGHT/dY)

        print(f"Камера настроена. Параметры: x = {self.x}, y = {self.y}, scale = {self.scale}")

    def move(self):
        self.x+=self.vx/self.scale
        self.y+=self.vy/self.scale
    def move_by_key(self,event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                self.vx=10
            elif event.key == pg.K_LEFT:
                self.vx=-10
            elif event.key == pg.K_UP:
                self.vy=-10
            elif event.key == pg.K_DOWN:
                self.vy=10
        elif event.type == pg.KEYUP:
            if event.key == pg.K_RIGHT:
                self.vx=0
            elif event.key == pg.K_LEFT:
                self.vx=0
            elif event.key == pg.K_UP:
                self.vy=0
            elif event.key == pg.K_DOWN:
                self.vy=0


    def Scale(self,event):
        if event.type == pg.MOUSEWHEEL:
            self.scale*=(1.1**event.y)

            
        
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
            
