"""Здесь все что касается нарисовать что-то на экране"""
import pygame as pg
import pyautogui
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
        self.flag=False
    def move(self,event):
        if event:
            if event.type==pg.MOUSEBUTTONDOWN and self.flag==False:
                in_x,in_y=self.x,self.y
                self.flag=True
                x,y = pyautogui.position()
            elif event.type==pg.MOUSEBUTTONUP and self.flag==True:
                self.flag=False
        x,y=pyautogui.position()
        in_x,in_y=self.x,self.y
        if self.flag==True:
            dx,dy = pyautogui.position()
            self.x,self.y=in_x+dx-x,in_y+dy-y

        

class ScreenDrawer():
    """Класс отвечающий за вывод на экран"""
    def __init__(self,screen):
        self.screen=screen
    def draw(self,cam):
        for i in Drawable.list_of_em:
            rel_x,rel_y=i.abs_x+cam.x,i.abs_y+cam.y
            if i.type=="circle":
                pg.draw.circle(self.screen, i.color, (rel_x, rel_y), 50*i.scale)
            
            
