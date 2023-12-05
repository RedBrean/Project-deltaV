"""Модуль в котором куча  физики"""
import math
from deltaV_vis import*
import copy
tick = 0
gravitational_constant = 6.674e-11


class SpaceObject:
    def __init__(self, x = 0, y : float = 0, vx : float = 0, vy:float = 0, m:float = 0, collisionR : float = 0) -> None:
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.m = m
        self.collisionR = collisionR 

    def move_by_gravity_of_spaceobjects_list(self, dt, AnotherSpaceObjects:list):
        """Изменяет скорость космического тела гравитацией других тел за время dt"""
        for spaceObject in AnotherSpaceObjects:
            if (self.x == spaceObject.x and self.y == spaceObject.y):
                continue
            Alpha = math.atan2(spaceObject.y - self.y, spaceObject.x - self.x)
            dV = dt*(gravitational_constant * spaceObject.m / ((spaceObject.x - self.x)**2 + (spaceObject.y - self.y)**2))
            self.vx += dV * math.cos(Alpha)
            self.vy += dV * math.sin(Alpha)
            if(tick % 500 == 0):
                pass
                #print(f"A:{Alpha}, dv = {dV}")
    
    def move(self, dt):
        self.x += self.vx *dt
        self.y += self.vy *dt

    def __str__(self):
        return f"{self.x}; {self.y}; {self.vx}; {self.vy}; {self.m}"
    
    def parse_from_list(self, parametrs):
        """Читает параметры с 0 до 5"""
        print(f"Reading parametrs: {parametrs}")

        self.x =  float(parametrs[0])
        self.y =  float(parametrs[1])
        self.vx = float(parametrs[2])
        self.vy = float(parametrs[3])
        self.m =  float(parametrs[4])
        self.collisionR = float(parametrs[5])
        print(f"Result = {self}")

class PhysicalModulation():    
    def __init__(self, space_objects : list[SpaceObject], copy_objects : bool = False):
        if not copy_objects:
            self.space_objects = space_objects
        else:
            self.space_objects = copy.deepcopy(space_objects)
        
    def update_by_dt(self, dt):
        """Двигает все за время dt"""
        for space_object in self.space_objects:
            space_object.move_by_gravity_of_spaceobjects_list(dt, self.space_objects)
            space_object.move(dt)

    def update_by_dt_few_times(self, dt, n : int):
        for _ in range(n):
            self.update_by_dt(dt)

