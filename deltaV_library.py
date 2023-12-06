"""модуль в котором класссы всякой мелочевки"""
import pygame as pg
import copy
from deltaV_physics import pg
from deltaV_vis import*
from deltaV_physics import*
from deltaV_settings import*
import math
import time

from deltaV_vis import pg


class GameObject(SpaceObject, Drawable):
    def __init__(self, x: float = 0, y: float = 0, vx: float = 0, vy: float = 0, m: float = 0) -> None:
        SpaceObject.__init__(self, x, y, vx, vy, m)
        self.color = WHITE
    @property
    def visualR(self):
        return self.collisionR
    
    def GetSurface(self, camera) -> pg.Surface:
        R = max(3, self.collisionR * camera.scale)
        width  = 2*R
        hight = 2*R
        surf = pg.Surface((width,hight))
        surf.fill(BLACK)
        surf.set_colorkey(BLACK)
        pg.draw.circle(surf, self.color, (width/2, hight/2), R)
        self.__visualR = (width**2 + hight**2)**0.5
        surf = surf.convert_alpha()
        return surf
    @property
    def visualR(self):
        try:
            return self.__visualR
        except:
            return 0

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
                 resolution = 100, dt = 3000, Tsim = 365*24*3600, needAutoOptimization = False, vanted_Iterations = 6000,
                 k_zamknutosti = 0.1, k_Tsim = 1.5, k_dt = 1):
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
        self.vanted_Iterations = vanted_Iterations
        self.calc_time = 0


        self.needAutoOptimization = needAutoOptimization
        #дефолтные коэфициенты оптимизации
        self.k_Tsim = k_Tsim 
        self.k_dt = k_dt
        self.vanted_Iterations = 6000
        self.k_zamknutosti = k_zamknutosti

        self.Restart_sim() #Возможно оно повторяяет часть конструктора, но так безопаснее


    @property
    def x(self):
        return self.reletive_object.x
    @property
    def y(self):
        return self.reletive_object.y

    @property
    def visualR(self):
        try:
#           return self.__visualR
            return 0
        except:
            return 0
    def Update(self, iteretions):
        #FIXME настройки и логика обновления пока сложны
        ticks_to_next_point = int(self.step - (self.tick % self.step))
        while (iteretions > ticks_to_next_point):
            x = self.my_main_object.x - self.my_reletive_object.x
            y = self.my_main_object.y - self.my_reletive_object.y
            self.new_trajectory_list.append((x, y))
            self.phys_sim.update_by_dt_few_times(self.dt, ticks_to_next_point)
            self.tick += ticks_to_next_point
            iteretions -= ticks_to_next_point

        self.phys_sim.update_by_dt_few_times(self.dt, iteretions)
        self.tick += iteretions

        if(self.tick > self.simTicks):
            self.trajectory_list = copy.copy(self.new_trajectory_list)
            self.Restart_sim()

    def Optimize(self, vantedIterations = 6000, k_zamknutosti = 0.1, k_dt = 1, k_Tsim = 1.5):
        #FIXME Надо сделать более адеватный рассчет времени обращения
        #dist = ((self.my_main_object.x - self.reletive_object.x)**2 + (self.my_main_object.y - self.reletive_object.y)**2)**0.5
        #V = ((self.my_main_object.vx - self.reletive_object.vx)**2 + (self.my_main_object.vy - self.reletive_object.vy)**2)**0.5
        #Tsim = 2*math.pi*dist/V
        #dt = Tsim//vantedIterations // 1
        #self.Tsim = Tsim * k_Tsim //1
        #self.dt = dt * k_dt // 1

        if (len(self.trajectory_list) > 1):

            maxX = self.trajectory_list[0][0]
            maxY = self.trajectory_list[0][1]
            minX = maxX
            minY = maxY
            for point in self.trajectory_list:
                if(point[0] > maxX):
                    maxX = point[0]
                if(point[0] < minX):
                    minX = point[0]
                if(point[1] > maxY):
                    maxY = point[1]
                if(point[1] < minY):
                    minY = point[1]
            dX = maxX-minX
            dY = maxY-minY
            needR = (dX**2 + dY**2)**0.5 * k_zamknutosti
            refX = self.trajectory_list[0][0]
            refY = self.trajectory_list[0][1]
            stage = 0 #0 - пока не удалились, 1 - удалились, 2 - приблизились и сократили время
            for i in range(1,len(self.trajectory_list)):
                point = self.trajectory_list[i]
                R = ((point[0]-refX)**2 + (point[1]-refY)**2)**0.5
                if(R > needR/k_zamknutosti/5):
                    stage = 1
                if(R<needR and stage==1):
                    self.Tsim = math.ceil(self.Tsim * i / len(self.trajectory_list)) * k_Tsim
                    stage = 2
                    break
            if stage<2:
                self.Tsim = math.ceil(self.Tsim*1.1)
        if (self.Tsim > 100*365*24*3600):
            self.Tsim = 80*365*24*3600
        self.dt = int(self.Tsim//vantedIterations // 1) * k_dt

    def Restart_sim(self):
        self.new_trajectory_list.clear()
        self.my_space_objects = copy.deepcopy(self.space_objects)
        self.my_main_object = self.my_space_objects[self.index_main_object]
        self.my_reletive_object = self.my_space_objects[self.index_reletive_object]
        self.phys_sim = PhysicalModulation(self.my_space_objects, False)

        self.tick = 0
        self.simTicks = self.Tsim//self.dt
        self.step = self.simTicks//self.resolution

        if(self.needAutoOptimization):
            self.Optimize(self.vanted_Iterations, self.k_zamknutosti, self.k_dt, self.k_Tsim)

    def GetSurface(self, camera) -> pg.Surface:
        #if(len(self.trajectory_list) == 0):
        #    surf = pg.Surface((10, 10))
        #    surf.set_colorkey(BLACK)
        #    surf.convert_alpha()
        #    return surf

        points = []
    
        camera_maxX = camera.x + WINDOW_WIDTH / camera.scale *2
        camera_minX = camera.x - WINDOW_WIDTH / camera.scale *2
        camera_maxY = camera.y + WINDOW_WIDTH / camera.scale *2
        camera_minY = camera.y - WINDOW_WIDTH / camera.scale *2
        for point in self.trajectory_list:
            #FIXME точки неприятно зацикливаются
            if(camera_minX < point[0] < camera_maxX and camera_minY < point[1] < camera_maxY):
                point_x = (point[0]*camera.scale)
                point_y = (point[1]*camera.scale)
                points.append((point_x, point_y))
        
        if(len(points) == 0):
            surf = pg.Surface((10, 10))
            surf.set_colorkey(BLACK)
            surf.convert_alpha()
            return surf

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
        if len(points) > 2:
            pg.draw.lines(surface, BLUE, False, points, 2)
        
        self.__visualR = (width ** 2 + hight**2)**0.5 / camera.scale

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
    def __init__(self, x: float = 0, y: float = 0, vx: float = 0, vy: float = 0, m: float = 0, angle = 0, a_0 = 5) -> None:
        super().__init__(x, y, vx, vy, m)

        self.thrust = 0
        self.angle = angle
        self.a_0 = a_0

        self.rotation_speed = 0
        self.thrust_increase = 0
        self.sprite = None
    
    def GetSurface(self, camera) -> pg.Surface:
        if(self.sprite  != None):
            surf = self.sprite
        else:
            surf = pg.Surface(20, 20)
            surf.fill(BLACK)
            surf.set_colorkey(BLACK)
            #FIXME надо нарисовать треугольник смотрящий вправо
            pg.draw.polygon(surf, WHITE, 
                    [[self.x, self.y+20], [self.x+50, self.y], 
                     [self.x, self.y-20]])
            surf.convert_alpha()

        return pg.transform.rotate(surf, self.angle)
    
    def Update(self):
        self.thrust+=self.thrust_increase
        self.angle+=self.rotation_speed
        if self.thrust>1:
            self.thrust = 1
        if self.angle>360:
            self.angle = self.angle % 360
    
    def move(self, dt):
        return super().move(dt)
        #FIXME Изменение скорости из-за работающей тяги

    def dynamic_change(self,event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                self.thrust_increase=0.05
            elif event.key == pg.K_s:
                self.thrust_increase=-0.05
            elif event.key == pg.K_a:
                self.rotation_speed=-10
            elif event.key == pg.K_d:
                self.rotation_speed=10
        elif event.type == pg.KEYUP:
            if event.key == pg.K_w:
                self.thrust_increase=0
            elif event.key == pg.K_s:
                self.thrust_increase=0
            elif event.key == pg.K_a:
                self.rotation_speed=0
            elif event.key == pg.K_d:
                self.rotation_speed=0

    def parse_from_list(self, parametrs):
        
        #0-5 координаты и скорость
        #sprite *название спрайта* если там оправдание отсутствия спрайта, то спрайта и не будет
        SpaceObject.parse_from_list(self, parametrs) #координаты, скорость и масса
        if(parametrs[6].split()[0] == "sprite"):
            self.sprite = pg.image.load(f"sprites/{parametrs[6].split()[1]}")
        
        
    
    
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


