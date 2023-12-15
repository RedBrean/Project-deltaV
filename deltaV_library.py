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
        if(R == 3):
            if hasattr(self, "sprite"):
                return self.sprite
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
            spriteFile = parametrs[7].split()
            if(spriteFile[0] == "sprite"):
                self.sprite = pg.image.load(f"sprites/{spriteFile[1]}")
                self.sprite = pg.transform.scale_by(self.sprite, 0.07)
        except:
            print("Что-то неладное в настройках отображения")
    

class Trajectory(Drawable):
    """Класс траектории Update обновляет внутренню симуляцию"""
    def __init__(self, space_objects : list[SpaceObject], main_object : SpaceObject, reletive_object : SpaceObject, 
                 resolution = 100, needAutoOptimization = False, vanted_Iterations = 6000, k_dt = 1, k_zamknutosti = 0.1):
        """ 
        аргументы: 
        dt - время шага расчета
        reolution - количество точек траектории
        Tsim - время симуляции"""
        self._index_main_object = space_objects.index(main_object)
        self._index_reletive_object = space_objects.index(reletive_object)

        self.space_objects = space_objects

        self.my_space_objects = []
        for space_object in self.space_objects:
            self.my_space_objects.append(SpaceObject.copy(space_object))

        self.my_main_object = self.my_space_objects[self._index_main_object]
        self.reletive_object = reletive_object
        self.my_reletive_object = self.my_space_objects[self._index_reletive_object]

        self.phys_sim = PhysicalModulation(self.my_space_objects, False)

        self.trajectory_list = []
        self.__new_trajectory_list = []

        self.resolution = resolution

        self.vanted_Iterations = vanted_Iterations
        self.calc_time = 0


        self.needAutoOptimization = needAutoOptimization
        #дефолтные коэфициенты оптимизации

        self.k_dt = k_dt
        self.vanted_Iterations = 6000
        self.k_zamknutosti = k_zamknutosti

        self.Restart_sim() #Возможно оно повторяяет часть конструктора, но так безопаснее

    @property
    def x(self):
        if(not self.custom_coord):
            return self.reletive_object.x
        else:
            return self.custom_x
        
    @property
    def y(self):
        if(not self.custom_coord):
            return self.reletive_object.y
        else:
            return self.custom_y

    @property
    def visualR(self):

        try:
            return self.__visualR
            return 0
        except:
            return 0
    def Update(self, iterations):
        """Обновляет внутреннюю симуляцию на несколько итераций"""
        for i in range(iterations):
            if(self.tick%self.point_step == 0):
                x = self.my_main_object.x - self.my_reletive_object.x
                y = self.my_main_object.y - self.my_reletive_object.y
                self.__new_trajectory_list.append((x, y))
            
            a = self.get_current_a_of_main_object(self.my_space_objects)
            ar = self.get_current_a_of_main_object([self.my_reletive_object])
            v = self.get_reletive_speed()
            r = ((self.my_main_object.x - self.my_reletive_object.x)**2 
                 + (self.my_main_object.y - self.my_reletive_object.y)**2)**0.5
            vanted_iterations = self.vanted_Iterations

            k1 = self.get_current_a_of_main_object([self.my_reletive_object]) / a
            k2 = 0

            k3 = 1 - k1
            try:
                dt1 = 2*math.pi * r / v / vanted_iterations
            except:
                dt1 = 0
                k1 = 0
            dt2 = 5 / (a*r)**0.5
            dt3 = 5 / a

            dt = self.k_dt*(dt1*k1 + dt2*k2 + dt3*k3)/(k1+k2+k3)

            dt  = min(self.k_dt*dt, 10**6)
            self.phys_sim.update_by_dt(dt)
            self.tick += 1

        if(self.tick > self.vanted_Iterations):
            self.trajectory_list = copy.copy(self.__new_trajectory_list)
            self.Restart_sim()

    def Optimize(self, k_zamknutosti = 0.2, k_dt_override = 1.2):
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
                    self.k_dt = math.ceil(self.k_dt * i / len(self.trajectory_list)) * k_dt_override
                    stage = 2
                    break
            if stage<2:
                self.k_dt = math.ceil(self.k_dt*1.2)
        if (self.k_dt > 1000):
            self.needAutoOptimization = False
            self.k_dt = 1

    def Restart_sim(self):
        self.__new_trajectory_list.clear()
        self.my_space_objects = []
        for space_object in self.space_objects:
            self.my_space_objects.append(SpaceObject.copy(space_object))

        self.my_main_object = self.my_space_objects[self._index_main_object]
        if isinstance(self.my_main_object, Player):
            self.my_main_object.thrust = 0
            #FIXME Костыль
        self.my_reletive_object = self.my_space_objects[self._index_reletive_object]
        self.phys_sim = PhysicalModulation(self.my_space_objects, False)

        self.tick = 0
        self.point_step = self.vanted_Iterations//self.resolution

        if(self.needAutoOptimization):
            self.Optimize(self.k_zamknutosti)

        self.custom_coord = False

    def GetSurface(self, camera) -> pg.Surface:
        if(len(self.trajectory_list) == 0):
            surf = pg.Surface((10, 10))
            surf.set_colorkey(BLACK)
            surf.convert_alpha()
            return surf

        points = []
    
        camera_maxX = camera.x + WINDOW_WIDTH  / camera.scale *2
        camera_minX = camera.x - WINDOW_WIDTH  / camera.scale *2
        camera_maxY = camera.y + WINDOW_HEIGHT / camera.scale *2
        camera_minY = camera.y - WINDOW_HEIGHT / camera.scale *2

        for i in range(len(self.trajectory_list)):
            #FIXME точки неприятно зацикливаются
            point = self.trajectory_list[i]
            if(camera_minX < point[0] + self.reletive_object.x < camera_maxX
                and camera_minY < point[1] + self.reletive_object.y < camera_maxY):
                point_x = (point[0]*camera.scale)
                point_y = (point[1]*camera.scale)
                points.append((point_x, point_y, i))
        
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

        width = 2*math.ceil(max(abs(maxX), abs(minX))) + 10
        hight = 2*math.ceil(max(abs(maxY), abs(minY))) + 10


        points = list(map(lambda p: (p[0] + width/2, p[1] + hight/2, p[2]), points))
    

        #self.trajectory_log_file.write(f"width : {width}\nhight: {hight}\n")

        surface = pg.Surface([width, hight])

        surface.fill(BLACK)
        surface.set_colorkey(BLACK)
        if len(points) > 2:
            prev_point = (0,0,-5)
            for point in points:
                color = BLUE
                if (hasattr(self, "color")):
                    color = self.color
                if(point[2] == prev_point[2]+1):
                    pg.draw.line(surface, color, prev_point[0:2], point[0:2], 4)
                prev_point = point
        
        self.__visualR = (width ** 2 + hight**2)**0.5 / camera.scale

        surface.convert_alpha()

        return surface

    def change_main_object(self, new_main_object):
        self._index_main_object = self.space_objects.index(new_main_object)
        self.Restart_sim()
        self.trajectory_list.clear()

    def change_reletive_object(self, new_rel_object):
        self.reletive_object = new_rel_object
        self._index_reletive_object = self.space_objects.index(new_rel_object)
        self.Restart_sim()
        self.trajectory_list.clear()

    def get_current_a_of_main_object(self, space_objects):
        main_object = self.my_main_object
        A = 0
        for spaceObject in space_objects:
            if (main_object.x == spaceObject.x and main_object.y == spaceObject.y):
                continue
            dA = (gravitational_constant * spaceObject.m) / ((spaceObject.x - main_object.x)**2 + (spaceObject.y - main_object.y)**2)
            A += dA
        return A

    def multiply_k_dt(self, k, needAutoOptimization = False):
        self.needAutoOptimization = needAutoOptimization
        self.k_dt *= k
        self.Restart_sim()
    def switch_optimization(self):
        self.needAutoOptimization = not self.needAutoOptimization
        self.Restart_sim()
    def set_k_dt(self, k_dt, needAutoOptimization = False):
        self.needAutoOptimization = needAutoOptimization
        self.k_dt = math.ceil(k_dt)
        self.Restart_sim()
    def get_reletive_speed(self):
        main_object = self.space_objects[self._index_main_object]
        reletive_object = self.space_objects[self._index_reletive_object]

        return ((main_object.vx - reletive_object.vx)**2 + (main_object.vy - reletive_object.vy)**2)**0.5
    

class Trajectory_old(Trajectory):
    """Старый рассчет  траектории. Точность постоянна"""
    def __init__(self, space_objects : list[SpaceObject], main_object : SpaceObject, reletive_object : SpaceObject, 
                 resolution = 500, dt = 3, Tsim = 10*3600, needAutoOptimization = False, vanted_Iterations = 6000,
                 k_zamknutosti = 0.1, k_Tsim = 1.5, k_dt = 1):
        """ 
        аргументы: 
        dt - время шага расчета
        reolution - количество точек траектории
        Tsim - время симуляции"""
        self._index_main_object = space_objects.index(main_object)
        self._index_reletive_object = space_objects.index(reletive_object)

        self.space_objects = space_objects
        """Космические объекты из реальлного мира"""

        self.my_space_objects = []
        """Космические объекты внутри симуляции траектории"""
        for space_object in self.space_objects:
            self.my_space_objects.append(SpaceObject.copy(space_object))

        self.my_main_object = self.my_space_objects[self._index_main_object]
        self.reletive_object = reletive_object
        self.my_reletive_object = self.my_space_objects[self._index_reletive_object]

        self.phys_sim = PhysicalModulation(self.my_space_objects, False)

        self.trajectory_list = []
        self.__new_trajectory_list = []

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

    def Update(self, iteretions):
        #FIXME настройки и логика обновления пока сложны
        ticks_to_next_point = int(self.step - (self.tick % self.step))
        while (iteretions > ticks_to_next_point):
            x = self.my_main_object.x - self.my_reletive_object.x
            y = self.my_main_object.y - self.my_reletive_object.y
            self.__new_trajectory_list.append((x, y))
            self.phys_sim.update_by_dt_few_times(self.dt, ticks_to_next_point)
            self.tick += ticks_to_next_point
            iteretions -= ticks_to_next_point

        self.phys_sim.update_by_dt_few_times(self.dt, iteretions)
        self.tick += iteretions

        if(self.tick > self.simTicks):
            self.trajectory_list = copy.copy(self.__new_trajectory_list)
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
                self.Tsim = math.ceil(self.Tsim*1.5)
        if (self.Tsim > 100*365*24*3600):
            self.Tsim = 80*365*24*3600
        self.dt = int(self.Tsim//vantedIterations // 1) * k_dt

    def Restart_sim(self):
        self.__new_trajectory_list.clear()
        self.my_space_objects = []
        for space_object in self.space_objects:
            self.my_space_objects.append(SpaceObject.copy(space_object))

        self.my_main_object = self.my_space_objects[self._index_main_object]
        if isinstance(self.my_main_object, Player):
            self.my_main_object.thrust = 0
            #FIXME Костыль
        self.my_reletive_object = self.my_space_objects[self._index_reletive_object]
        self.phys_sim = PhysicalModulation(self.my_space_objects, False)

        self.tick = 0
        self.dt = math.ceil(self.Tsim//self.vanted_Iterations)
        self.dt = max(self.dt, 1)
        self.simTicks = math.ceil(self.Tsim//self.dt)
        self.step = self.simTicks//self.resolution

        if(self.needAutoOptimization):
            self.Optimize(self.vanted_Iterations, self.k_zamknutosti, self.k_dt, self.k_Tsim)

        self.custom_coord = False

    def multiply_T_sim(self, k, needAutoOptimization = False):
        self.needAutoOptimization = needAutoOptimization
        self.Tsim *= k
        self.Restart_sim()

    def set_Tsim_in_years(self, years, needAutoOptimization = False):
        self.needAutoOptimization = needAutoOptimization
        self.Tsim = math.ceil(years*365*24*3600)
        self.Restart_sim()

class Player(GameObject):
    def __init__(self, x: float = 0, y: float = 0, vx: float = 0, vy: float = 0, m: float = 0, angle = 0, a_0 = 10) -> None:
        super().__init__(x, y, vx, vy, m)

        self.thrust = 0
        self.angle = angle
        self.a_0 = a_0

        self.rotation_speed = 0
        self.thrust_increase = 0
        self.sprite = None
        self.sprite_no_thrust = None
        self.deltaV = math.inf
    def GetSurface(self, camera) -> pg.Surface:
        if (self.sprite != None):
            if self.sprite_no_thrust != None and self.thrust == 0:
                surf = self.sprite_no_thrust
            else:
                surf = self.sprite

        else:
            surf = pg.Surface((20, 20))
            surf.fill(BLACK)
            surf.set_colorkey(BLACK)
            #FIXME надо нарисовать треугольник смотрящий вправо
            pg.draw.polygon(surf, YELLOW, 
                    [[0, 5], [20, 10], 
                     [0, 15]])
            surf.convert_alpha()

        return pg.transform.rotate(surf, self.angle)
    
    def Update(self):
        self.thrust+=self.thrust_increase
        self.angle+=self.rotation_speed
        
        if self.thrust>1:
            self.thrust = 1
        if self.thrust<-1:
            self.thrust = -1
        if self.angle>360:
            self.angle = self.angle % 360
        if self.deltaV <= 0:
            self.thrust = 0
            self.deltaV = 0
    
    def move(self, dt):
        super().move(dt)
        #FIXME Изменение скорости из-за работающей тяги
        self.deltaV -= abs(self.thrust*self.a_0*dt)
        self.vx+=self.thrust*self.a_0*math.cos(self.angle*math.pi/180)
        self.vy-=self.thrust*self.a_0*math.sin(self.angle*math.pi/180)

    def dynamic_change(self,event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                self.thrust_increase=0.02
            elif event.key == pg.K_s:
                self.thrust_increase=-0.02
            elif event.key == pg.K_a:
                self.rotation_speed+=3
            elif event.key == pg.K_d:
                self.rotation_speed-=3
        elif event.type == pg.KEYUP:
            if event.key == pg.K_w:
                self.thrust_increase=0
                self.thrust = 0 #FIXME костыль
            elif event.key == pg.K_s:
                self.thrust_increase=0
                self.thrust = 0 #FIXME костыль
            elif event.key == pg.K_a:
                self.rotation_speed=0
            elif event.key == pg.K_d:
                self.rotation_speed=0

    def parse_from_list(self, parametrs):
        
        #0-5 координаты и скорость
        #sprite *название спрайта* если там оправдание отсутствия спрайта, то спрайта и не будет
        SpaceObject.parse_from_list(self, parametrs) #координаты, скорость и масса
        if(parametrs[6].split()[0] == "deltaV"):
            self.deltaV = float(parametrs[6].split()[1])
        try:
            if(parametrs[7].split()[0] == "sprite"):
                self.sprite = pg.image.load(f"sprites/{parametrs[7].split()[1]}")
                self.sprite = pg.transform.rotate(self.sprite, 3)
                self.sprite = pg.transform.scale_by(self.sprite, 0.05)
            if(parametrs[8].split()[0] == "sprite_no_thrust"):
                self.sprite_no_thrust = pg.image.load(f"sprites/{parametrs[8].split()[1]}")
                self.sprite_no_thrust = pg.transform.rotate(self.sprite_no_thrust, 4)
               
                self.sprite_no_thrust = pg.transform.scale_by(self.sprite_no_thrust, 0.05)

        except:
            print("Штирлиц отбивал шифровку в штаб. Он не знал азбуки морзе, \n но по радостному пиликанию в штабе поняли - Задание Партии выполнено")
            
    
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


