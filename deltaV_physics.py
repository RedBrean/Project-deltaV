"""Модуль в котором куча  физики"""
import math

gravitational_constant = 6.674e-11


class SpaceObject():
    def __init__(self, x : float = 0, y : float = 0, vx : float = 0, vy:float = 0, m:float = 0) -> None:
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.m = m

    def move_by_gravity_of_spaceobjects_list(self, dt, AnotherSpaceObjects:list):
        """Изменяет скорость космического тела гравитацией других тел за время dt"""
        for spaceObject in AnotherSpaceObjects:
            if (self.x == spaceObject.x and self.y == spaceObject.y):
                continue
            Alpha = math.atan2(spaceObject.y - self.y, spaceObject.x - self.x)
            (spaceObject.x - self.x)**2 + (spaceObject.y - self.y)**2
            dV = dt*(gravitational_constant * spaceObject.M
                            / ((spaceObject.x - self.x)**2 + (spaceObject.y - self.y)**2))
            self.vx += dV * math.cos(Alpha)
            self.vy += dV * math.sin(Alpha)
    def __str__(self):
        return f"{self.x}; {self.y}; {self.vx}; {self.vy}; {self.m}"
    
    def parse_from_str(self, string):
        paramtetrs = string.split("; ")
        self.x =  float(paramtetrs[0])
        self.y =  float(paramtetrs[1])
        self.vx = float(paramtetrs[2])
        self.vy = float(paramtetrs[3])
        self.m =  float(paramtetrs[4])

class PhysicalModulation():    
    def __init__(self, space_objects:list[SpaceObject]):
        self.space_objects = space_objects.copy()
        
    def update_by_dt(self, dt):
        """Двигает все за время dt"""
        for space_object in self.space_objects:
            space_object.move_by_gravity_of_spaceobjects_list(dt, self.space_objects)