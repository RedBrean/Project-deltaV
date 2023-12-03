"""модуль в котором класссы всякой мелочевки"""
import pygame as pg
import copy
from deltaV_vis import*
from deltaV_physics import*
from deltaV_settings import*


class GameObject(SpaceObject, Drawable):
    def __init__(self, x: float = 0, y: float = 0, vx: float = 0, vy: float = 0, m: float = 0) -> None:
        SpaceObject.__init__(self, x, y, vx, vy, m)
        self.color = WHITE
    def GetSurface(self, camera) -> pg.Surface:
        R = max(3, self.collisionR * camera.scale)
        width  = 3*R
        hight = 3*R
        surf = pg.Surface((width,hight))
        surf.fill(BLACK)
        surf.set_colorkey(BLACK)
        pg.draw.circle(surf, self.color, (width/2, hight/2), R)
        surf = surf.convert_alpha()
        return surf
    def parse_from_list(self, parametrs):
        super().parse_from_list(parametrs)
        try:
            spriteSettings = parametrs[6].split()
            if(spriteSettings[0] == "color"):
                self.color = color_from_str(spriteSettings[1])
        except:
            print("Что-то неладное в настройках отображения")
    

class Trajectory(Drawable):
    def __init__(self, space_objects : list[SpaceObject], main_object : SpaceObject, reletive_object : SpaceObject = None):
        self.space_objects = copy.deepcopy(space_objects)
        self.phys_sim = PhysicalModulation(space_objects)

        #FIXME как хранить основные объекты?.. 

        self.trajectory_list = []
        pass

    def Update(self):
        #FIXME настройки и логика обновления пока сложны
        for _ in range(10000):

            self.trajectory_list.append
    
    def GetSurface(self, camera) -> pg.Surface:
        pass
    
    def GetRect(self, camera) -> pg.Rect:
        pass

class Player(GameObject):
    def __init__(self, x: float = 0, y: float = 0, vx: float = 0, vy: float = 0, m: float = 0) -> None:
        super().__init__(x, y, vx, vy, m)


class Button():
    """Класс кнопки"""
    def __init__(self,rect,action,host_object):
        self.action = action
        self.rect = rect
        self.host_object = host_object
        self.width = rect.width
        self.height = rect.height
    def try_pressing(self,event):
        if event.button == 1:
            if (event.pos[0]<self.rect.bottomright[0]):
                if (event.pos[1]<self.rect.bottomright[1]):
                    if (event.pos[0]>self.rect.topleft[0]):
                        if (event.pos[1]<self.rect.topleft[1]):
                            self.action()
    def update(self):
        self.rect.topleft[0] = self.host_object.x-self.width/2
        self.rect.topleft[1] = self.host_object.y-self.height/2
        self.rect.bottomright[0] = self.rect.topleft[0]+self.width
        self.rect.bottomright[1] = self.rect.topleft[1]+self.height


