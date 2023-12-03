"""модуль в котором класссы всякой мелочевки"""
import pygame as pg
import copy
from deltaV_vis import*
from deltaV_physics import*
from deltaV_settings import*
import math
import time


class GameObject(SpaceObject, Drawable):
    def __init__(self, x: float = 0, y: float = 0, vx: float = 0, vy: float = 0, m: float = 0) -> None:
        SpaceObject.__init__(self, x, y, vx, vy, m)
        self.color = WHITE
    def GetSurface(self, camera) -> pg.Surface:
        R = max(3, self.collisionR * camera.scale)
        width  = 2*R
        hight = 2*R
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
    def __init__(self, space_objects : list[SpaceObject], main_object : SpaceObject, reletive_object : SpaceObject, 
                 resolution = 100, dt = 1000, Tsim = 365*24*3600):
        """ 
        аргументы: 
        dt - время шага расчета
        reolution - количество точек траектории
        Tsim - время симуляции"""
        self.__index_main_object = space_objects.index(main_object)
        self.__index_reletive_object = space_objects.index(reletive_object)

        self.space_objects = space_objects
        self.my_space_objects = copy.deepcopy(space_objects)
        self.my_main_object = self.my_space_objects[self.__index_main_object]
        self.reletive_object = reletive_object
        self.my_reletive_object = self.my_space_objects[self.__index_reletive_object]

        self.phys_sim = PhysicalModulation(self.my_space_objects, False)

        self.trajectory_list = []
        self.new_trajectory_list = []

        self.resolution = resolution
        self.dt = dt
        self.Tsim = Tsim
        self.calc_time = 0


    @property
    def x(self):
        return self.reletive_object.x
    @property
    def y(self):
        return self.reletive_object.y

    def Update(self, resolution_ticks):
        #FIXME настройки и логика обновления пока сложны
        update_times = math.floor(self.Tsim/self.resolution/self.dt)
        for _ in range(resolution_ticks):
            self.phys_sim.update_by_dt_few_times(self.dt, update_times)
            x = self.my_main_object.x - self.my_reletive_object.x
            y = self.my_main_object.y - self.my_reletive_object.y

            self.new_trajectory_list.append((x, y))
            self.calc_time += self.dt*update_times
        
        if(self.calc_time > self.Tsim):
            self.trajectory_list = copy.copy(self.new_trajectory_list)
            self.Restart_sim()


    def Restart_sim(self):
            self.new_trajectory_list.clear()
            self.calc_time = 0
            self.my_space_objects = copy.deepcopy(self.space_objects)
            self.my_main_object = self.my_space_objects[self.__index_main_object]
            self.my_reletive_object = self.my_space_objects[self.__index_reletive_object]
            self.phys_sim = PhysicalModulation(self.my_space_objects, False)

    def GetSurface(self, camera) -> pg.Surface:
        if(len(self.trajectory_list) == 0):
            return pg.Surface((10, 10))

        points = []

        for point in self.trajectory_list:
            point_x = (point[0]*camera.scale)
            point_y = (point[1]*camera.scale)
            points.append((point_x, point_y))

        maxX = points[0][0]
        maxY = points[0][1]
        minX = maxX
        minY = maxY
        for point in points:
            if(point[0] > maxX):
                maxX = point[0]
            if(point[0] < minX):
                minX = point[0]
            if(point[1] > maxY):
                maxY = point[1]
            if(point[1] < minY):
                minY = point[1]

        width = max(1.2*math.ceil(maxX - minX), 1)
        hight = max(1.2*math.ceil(maxY - minY), 1)

        points = list(map(lambda p: (p[0] + width/2, p[1] + hight/2), points))
        
        surface = pg.Surface([width, hight])

        surface.fill(BLACK)
        surface.set_colorkey(BLACK)
        pg.draw.lines(surface, BLUE, False, points, 2)
        
        surface.convert_alpha()

        end_time = time.time()

        return surface



class Player(GameObject):
    def __init__(self, x: float = 0, y: float = 0, vx: float = 0, vy: float = 0, m: float = 0) -> None:
        super().__init__(x, y, vx, vy, m)
    

class Button():
    """Класс кнопки"""
    def __init__(self):
        pass

