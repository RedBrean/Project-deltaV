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
        self.index_main_object = space_objects.index(main_object)
        self.index_reletive_object = space_objects.index(reletive_object)

        self.space_objects = space_objects
        self.my_space_objects = copy.deepcopy(space_objects)
        self.my_main_object = self.my_space_objects[self.index_main_object]
        self.reletive_object = reletive_object
        self.my_reletive_object = self.my_space_objects[self.index_reletive_object]

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
        for _ in range(math.ceil(resolution_ticks)):
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
        self.my_main_object = self.my_space_objects[self.index_main_object]
        self.my_reletive_object = self.my_space_objects[self.index_reletive_object]
        self.phys_sim = PhysicalModulation(self.my_space_objects, False)

    def GetSurface(self, camera) -> pg.Surface:
        if(len(self.trajectory_list) == 0):
            surf = pg.Surface((10, 10))
            surf.set_colorkey(BLACK)
            surf.convert_alpha()
            return surf

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

        width = max(2*math.ceil(abs(maxX) + abs(minX)), 1)
        hight = max(2*math.ceil(abs(maxY) + abs(minY)), 1)

        points = list(map(lambda p: (p[0] + width/2, p[1] + hight/2), points))
        
        surface = pg.Surface([width, hight])

        surface.fill(BLACK)
        surface.set_colorkey(BLACK)
        pg.draw.lines(surface, BLUE, False, points, 2)
        
        surface.convert_alpha()

        return surface

    def change_main_object(self, new_main_object):
        self.index_main_object = self.space_objects.index(new_main_object)
        self.Restart_sim()
        self.trajectory_list.clear()

    
    def change_reletive_object(self, new_rel_object):
        self.reletive_object = new_rel_object
        self.index_reletive_object = self.space_objects.index(new_rel_object)
        self.Restart_sim()
        self.trajectory_list.clear()

class Player(GameObject):
    def __init__(self, x: float = 0, y: float = 0, vx: float = 0, vy: float = 0, m: float = 0) -> None:
        super().__init__(x, y, vx, vy, m)
    
class Buttons():
    """Класс множества кнопок"""
    def __init__(self):
        self.buttons : list[Button] = []
    
    def append(self, button):
        self.buttons.append(button)

    def try_pressing(self, event):
        for cButton in self.buttons:
            cButton.try_pressing(event)
    
    def update(self):
        for cButton in self.buttons:
            cButton.update()

class Button():
    """Класс кнопки"""
    def __init__(self, rect : pg.rect.Rect, action, arg = None, camera: Camera = None, mouse_button = 1,host_object : Drawable = None):
        self.action = action
        self.rect = rect
        self.host_object = host_object
        self.mouse_button = mouse_button
        self.camera = camera
        self.arg = arg

        self.__has_host = not(host_object == None or camera == None)
        if(self.__has_host):
            self.x_rel = self.rect.centerx
            self.y_rel = self.rect.centery

            self.y0 = host_object.y


    
    def try_pressing(self,event):
        if event.button == self.mouse_button:
            if (self.rect.contains(event.pos, (1, 1))):
                if(self.arg == None):
                    self.action()
                else:
                    self.action(self.arg)
                
    def update(self):
        if(self.__has_host):
            host_coord = self.camera.get_screen_coord(self.host_object) 
            self.rect.center = (host_coord[0]+self.x_rel, host_coord[1]+self.y_rel)


