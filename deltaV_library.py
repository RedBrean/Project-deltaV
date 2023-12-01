"""модуль в котором класссы всякой мелочевки"""
import pygame as pg
from deltaV_vis import*
from deltaV_physics import*


class GameObject(SpaceObject, Drawable):
    def __init__(self, x: float = 0, y: float = 0, vx: float = 0, vy: float = 0, m: float = 0) -> None:
        SpaceObject.__init__(self, x, y, vx, vy, m)
    def GetSurface(self, camera) -> pg.Surface:
        R = max(3, self.collisionR * camera.scale)
        width  = 3*R
        hight = 3*R
        surf = pg.Surface((width,hight))
        surf.fill(BLACK)
        surf.set_colorkey(BLACK)
        pg.draw.circle(surf, WHITE, (width/2, hight/2), R)
        surf = surf.convert_alpha()
        return surf
    

class Player(GameObject):
    def __init__(self, x: float = 0, y: float = 0, vx: float = 0, vy: float = 0, m: float = 0) -> None:
        super().__init__(x, y, vx, vy, m)


class Button():
    """Класс кнопки"""
    def __init__(self):
        pass

