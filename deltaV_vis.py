"""Здесь все что касается нарисовать что-то на экране"""
import pygame as pg
from deltaV_settings import *
import copy

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
        """Плохой метод, не оптимизирован"""
        #должно понимать где оно должно рисовать
        x = (self.x-camera.x)*camera.scale + WINDOW_WIDTH/2
        y = (self.y-camera.y)*camera.scale + WINDOW_HEIGHT/2
        #FIXME Сейчас прямоугольник всегда 50 на 50
        rect = self.GetSurface(camera).get_rect()
        rect.center = (x,y)
        return rect
    
    def GetRectWihtSurf(self, surface : pg.Surface, camera):
        #должно понимать где оно должно рисовать
        x = (self.x-camera.x)*camera.scale + WINDOW_WIDTH/2
        y = (self.y-camera.y)*camera.scale + WINDOW_HEIGHT/2
        #FIXME Сейчас прямоугольник всегда 50 на 50
        rect = surface.get_rect()
        rect.center = (x,y)
        return rect
    
    def Get_Surf_and_Rect(self, camera):
        surface = self.GetSurface(camera)
        rect = self.GetRectWihtSurf(surface, camera)
        return surface, rect
        
class Camera():
    def __init__(self,x=0,y=0):
        self.pivotx = 0
        self.pivoty = 0

        self.relx = 0
        self.rely = 0

        self.x=x
        self.y=y

        self.vx=0
        self.vy=0
        self.scale = 1

        self.has_pivot = False
        self.pivot_object = None

    @property
    def x(self):
        return self.relx + self.pivotx
    @property
    def y(self):
        return self.rely + self.pivoty
    @x.setter
    def x(self, value):
        self.relx += value - self.x
    @y.setter
    def y(self, value):
        self.rely += value - self.y

    def get_screen_coord(self, draweble_object : Drawable):
        return((draweble_object.x - self.x)*self.scale + WINDOW_WIDTH//2, 
               (draweble_object.y - self.y)*self.scale + WINDOW_HEIGHT//2)
    

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

        self.has_pivot = False

    def Update(self):
        self.relx+=self.vx/self.scale
        self.rely+=self.vy/self.scale

        if(self.has_pivot):
            self.pivotx = self.pivot_object.x
            self.pivoty = self.pivot_object.y

    def SetPivot(self, pivotObject):
        self.pivot_object = pivotObject
        self.has_pivot = True
        self.relx = 0
        self.rely = 0


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
        self.drawble_objects=copy.copy(drawble_objects)
    
    def append_object(self, draweble_object : Drawable):
        self.drawble_objects.append(draweble_object)
    
    def draw(self, camera : Camera):
        #Проходит по всем объектам в списке этого же класса и рисует их
        self.screen.fill(BLACK)
        maxX = camera.x + WINDOW_WIDTH / camera.scale / 2
        minX = camera.x - WINDOW_WIDTH / camera.scale / 2
        maxY = camera.y + WINDOW_WIDTH / camera.scale / 2
        minY = camera.y - WINDOW_WIDTH / camera.scale / 2

        for cDrawebleObject in self.drawble_objects:
            #FIXME тут костыль с collisionR
            try:            
                if(minX < cDrawebleObject.x + cDrawebleObject.collisionR
                    and cDrawebleObject.x - cDrawebleObject.collisionR < maxX 
                    and minY < cDrawebleObject.y + cDrawebleObject.collisionR
                    and cDrawebleObject.y - cDrawebleObject.collisionR < maxY):
                    surf, rect = cDrawebleObject.Get_Surf_and_Rect(camera)
                    self.screen.blit(surf, rect)
            except:
                if(minX < cDrawebleObject.x < maxX and minY < cDrawebleObject.y < maxY):
                    surf, rect = cDrawebleObject.Get_Surf_and_Rect(camera)
                    self.screen.blit(surf, rect)

            
