"""Только в этом модуле можно предпринмать какие-то активные действия.
 Остальные модули по сути служат библиотекой, в них стараемся не писать ничего что не является функцией или классом"""

import pygame as pg
 
import deltaV_test

from deltaV_vis import *
from deltaV_library import*
from deltaV_input_output import*
from deltaV_physics import*
from deltaV_settings import*
#settings


gameStage = 0
"""Переменная текущего состояния игры. 
0 - еще не играем
1 - играем
2 - результат
Может меняться"""


while gameStage==0:
    #первоначальная настройка
    pg.init()
    deltaV_test.testInit()
    clock = pg.time.Clock() 
    screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    
    #установка шрифтов. Размер зависит от экрана, числа 36 и 25 подогнанны 
    f1 = pg.font.Font(None, int(round(WINDOW_HEIGHT*36/850)))
    f2 = pg.font.Font(None, int(round(WINDOW_HEIGHT*25/850))) 
    pg.font.init()


    WH = WINDOW_HEIGHT
    WW = WINDOW_WIDTH


    #скорости симуляции
    # 1 число - количество итераций симуляции за тик, 2 число - шаг dt симуляции
    time_coefficients = [[1,1], [100,1], [100,5], [100,20], [100,50], [100,100], [100, 200], [100, 500], [200, 500], [500, 1000], [500, 2000], [500, 4000]]
    time_coefficient_number = 0

    time_coefficient = time_coefficients[time_coefficient_number]
    trajectory_K_dts = [1, 2, 3, 5, 10, 50, 100, 500]

    trajectory_Tsims = [0.01, 0.02, 0.05, 0.1, 0.3, 0.6, 1, 2, 4]
 
    
    objects = read_level_from_file(file_name)
    drawer = ScreenDrawer(screen,objects)

    cam = Camera()
    cam.set_up_defoult(objects)

    mainPhisMod = PhysicalModulation(objects)

    player = None
    for cObject in objects:
        if isinstance(cObject, Player):
            player = cObject
            break
    if(player == None):
        print("Нет игрока!")
    if (player != None):
        trajectory1 = Trajectory(objects, player, objects[3], needAutoOptimization=False)
        trajectory2 = Trajectory_old(objects, player, objects[3], needAutoOptimization=True)
        trajectory = trajectory1
        cam.SetPivot(player)
        if(EARCH_DEFOULT):
            cam.scale *= 20000
            trajectory.change_reletive_object(objects[3])
    else:
        trajectory = Trajectory(objects, objects[3], objects[0], needAutoOptimization=False)

    drawer.append_object(trajectory)

    buttons = Buttons()

    #добавляем кнопки на планеты для привязки
    for cObject in objects:
        rect = pg.rect.Rect((0,0), (30, 30))
        rect.center = (0, 0)
        button = Button(rect, cam.SetPivot, cObject, cam, host_object=cObject)

        buttons.append(button)

    for cObject in objects:
        rect = pg.rect.Rect((0,0), (30, 30))
        rect.center = (0, 0)
        button1 = Button(rect, trajectory1.change_reletive_object, cObject, cam, mouse_button=3, host_object=cObject)
        button2 = Button(rect, trajectory2.change_reletive_object, cObject, cam, mouse_button=3, host_object=cObject)
        buttons.append(button1)
        buttons.append(button2)
    
    #настройка траектории

    trajectory1.vanted_Iterations = TRAJECTORY_VANTED_ITERATIONS
    trajectory1.k_zamknutosti = TRAJECTORY_K_ZAMKNUTOSTI
    trajectory1.k_Tsim = TRAJECTORY_K_T_SIM
    trajectory1.needAutoOptimization = TRAJECTORY_AUTO_OPTIMIZATION
    trajectory1.resolution = TRAJECTORY_RESOLUTION
    
    trajectory2.vanted_Iterations = TRAJECTORY_VANTED_ITERATIONS
    trajectory2.k_zamknutosti = TRAJECTORY_K_ZAMKNUTOSTI
    trajectory2.k_Tsim = TRAJECTORY_K_T_SIM
    trajectory2.needAutoOptimization = TRAJECTORY_AUTO_OPTIMIZATION
    trajectory2.resolution = TRAJECTORY_RESOLUTION
    trajectory2.color = RED

    gameStage = 1

def switch_trajectory():
    global trajectory, trajectory1, trajectory2, drawer
    drawer.drawble_objects.remove(trajectory)
    if(trajectory == trajectory1):
        trajectory = trajectory2
    else:
        trajectory = trajectory1
    drawer.drawble_objects.append(trajectory)

    trajectory.Restart_sim()

def trajectory_settings_set(index):
    if(trajectory == trajectory1):
        trajectory1.set_k_dt(trajectory_K_dts[index])
    else:
        trajectory2.set_Tsim_in_years(trajectory_Tsims[index])


def trajectory_settings_mult(k):
    if(trajectory == trajectory1):
        trajectory1.multiply_k_dt(k)
    else:
        trajectory2.multiply_k_dt(k)
while gameStage==1: 

    time_coefficient = time_coefficients[time_coefficient_number]
    
    thrust = player.thrust

    #обновялем физическую симуляцию на уставновленной скорости симуляции
    mainPhisMod.update_by_dt_few_times(time_coefficient[1], time_coefficient[0])
    
    buttons.update()
    


    for event in pg.event.get():
        if event.type == pg.QUIT:
            gameStage="No"
        elif event.type == pg.KEYDOWN:
            cam.move_by_key(event)
            try:
                player.dynamic_change(event)
            except:
                pass

            if event.key == pg.K_TAB:
                cam.has_pivot = False
            if event.key == pg.K_EQUALS:
                if time_coefficient_number<len(time_coefficients)-1:
                    time_coefficient_number+=1
            if event.key == pg.K_MINUS:
                if time_coefficient_number>0:
                    time_coefficient_number-=1
            if event.key == pg.K_0:
                time_coefficient_number=0
            if event.key == pg.K_o:
                trajectory.switch_optimization()
            if event.key == pg.K_1:
                trajectory_settings_set(0)
            if event.key == pg.K_2:
                trajectory_settings_set(1)
            if event.key == pg.K_3:
                trajectory_settings_set(2)
            if event.key == pg.K_4:
                trajectory_settings_set(3)
            if event.key == pg.K_5:
                trajectory_settings_set(4)
            if event.key == pg.K_6:
                trajectory_settings_set(5)
            if event.key == pg.K_7:
                trajectory_settings_set(6)
            if event.key == pg.K_8:
                trajectory_settings_set(7)

            if event.key == pg.K_i:
                trajectory_settings_mult(1.2)
            if event.key == pg.K_u:
                trajectory_settings_mult(1/1.2)
            if event.key == pg.K_j:
                switch_trajectory()

        elif event.type == pg.KEYUP:
            cam.move_by_key(event)
            try:
                player.dynamic_change(event)
            except:
                pass
        elif event.type == pg.MOUSEBUTTONDOWN:
            buttons.try_pressing(event)
        else:
            pass
        cam.Scale(event)
    
    cam.Update()

    try:
        player.Update()
    except:
        pass

    trajectory.Update(TRAJECTORY_UPDATES_PER_TICK)


    drawer.draw(cam)

    #вывод скорости симуляции в формате без кучи нулей
    if time_coefficient[1]*time_coefficient[0] <1000:
        text1 = f1.render(str(time_coefficient[1]*time_coefficient[0])+"X", 1, (255,255,255))
    elif time_coefficient[1]*time_coefficient[0] <1000000:
        text1 = f1.render(str((time_coefficient[1]*time_coefficient[0])//1000)+"kX", 1, (255,255,255))
    elif time_coefficient[1]*time_coefficient[0] >=1000000:
        text1 = f1.render(str((time_coefficient[1]*time_coefficient[0])//1000000)+"MX", 1, (255,255,255))

    #вывод управления
    text2 = f1.render("Тяга: "+str(round(player.thrust,2)), 1, (255,255,255))
    text3 = f2.render("управление: WASD - ракета, ",1,(255,255,255))
    text4 = f2.render("стрелки - камера, скролл - масштабирование, +/- время ",1,(255,255,255))
    text5 = f2.render("Цифры 1-8 - предустановленные длины траектории",1,(255,255,255))
    text9 = f2.render("ЛКМ, ПКМ - привязка камеры/траектории",1,(255,255,255))

    text6 = f2.render("u - добавить длину,i - убавить длину, o - замкнуть траекторию, j - другой движок траектории",1,(255,255,255))
    
    #вывод остатка топлива
    try:
        text7 = f1.render("DeltaV: "+str(round(player.deltaV))+" m/s",1,(255,255,255))
    except:
        text7 = f1.render("DeltaV не ограничена!",1,(255,255,255))
    
    #вывод относительной скорости
    text8 = f1.render(str(round(trajectory.get_reletive_speed())) +" m/s",1,(255,255,255))

    #вывод текстов на экран в относительных коорднатах 
    screen.blit(text1, (WW*1/100, WH*2/50))
    screen.blit(text2, (WW*82/100, WH*3/50))
    screen.blit(text3, (WW/100, WH*45/50))
    screen.blit(text4, (WW/100, WH*46/50))
    screen.blit(text5, (WW/100, WH*47/50))
    screen.blit(text6,(WW/100, WH*48/50))
    screen.blit(text9,(WW/100, WH*49/50))
    screen.blit(text7, (WW*82/100, WH/50))
    screen.blit(text8,(WW*87/100, WH*47/50))
    pg.display.update()
    clock.tick(150)
    




pg.quit()