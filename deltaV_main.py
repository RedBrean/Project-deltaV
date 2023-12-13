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

    f1 = pg.font.Font(None, int(round(WINDOW_HEIGHT*36/850)))
    f2 = pg.font.Font(None, int(round(WINDOW_HEIGHT*25/850))) 
    pg.font.init()
    WH = WINDOW_HEIGHT
    WW = WINDOW_WIDTH
    



    time_coefficients = [[1,1], [100,1], [100,5], [100,20], [100,50], [100,100], [100, 200], [100, 500], [200, 500], [500, 1000], [500, 2000], [500, 4000]]
    time_coefficient_number = 0
    #1,100, 1000, 2500, 5000,10000, 25000, 50000, 100000, 500000, 1m
    time_coefficient = time_coefficients[time_coefficient_number]
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
        trajectory = Trajectory(objects, player, objects[0], needAutoOptimization=False, k_Tsim=1.1)
        cam.SetPivot(player)
        if(EARCH_DEFOULT):
            cam.scale *= 20000
            trajectory.change_reletive_object(objects[3])
            trajectory.set_Tsim_in_years(0.005)
    else:
        trajectory = Trajectory(objects, objects[3], objects[0], needAutoOptimization=False, k_Tsim=1.1)

    drawer.append_object(trajectory)

    buttons = Buttons()
    for cObject in objects:
        rect = pg.rect.Rect((0,0), (30, 30))
        rect.center = (0, 0)
        button = Button(rect, cam.SetPivot, cObject, cam, host_object=cObject)

        buttons.append(button)


    for cObject in objects:
        rect = pg.rect.Rect((0,0), (30, 30))
        rect.center = (0, 0)
        button = Button(rect, trajectory.change_reletive_object, cObject, cam, mouse_button=3, host_object=cObject)

        buttons.append(button)
    

    trajectory.vanted_Iterations = VANTED_ITERATIONS
    trajectory.k_zamknutosti = 0.2
    trajectory.k_Tsim = 1.5
    trajectory.needAutoOptimization = True
    gameStage = 1


while gameStage==1: 

    time_coefficient = time_coefficients[time_coefficient_number]
    
    thrust = player.thrust


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
                trajectory.set_Tsim_in_years(trajectory_Tsims[0])
            if event.key == pg.K_2:
                trajectory.set_Tsim_in_years(trajectory_Tsims[1])
            if event.key == pg.K_3:
                trajectory.set_Tsim_in_years(trajectory_Tsims[2])
            if event.key == pg.K_4:
                trajectory.set_Tsim_in_years(trajectory_Tsims[3])
            if event.key == pg.K_5:
                trajectory.set_Tsim_in_years(trajectory_Tsims[4])
            if event.key == pg.K_6:
                trajectory.set_Tsim_in_years(trajectory_Tsims[5])
            if event.key == pg.K_7:
                trajectory.set_Tsim_in_years(trajectory_Tsims[6])
            if event.key == pg.K_8:
                trajectory.set_Tsim_in_years(trajectory_Tsims[7])
            if event.key == pg.K_i:
                trajectory.multiply_T_sim(1.2)
            if event.key == pg.K_u:
                trajectory.multiply_T_sim(1/1.2)
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

    trajectory.Update(200)

    print(trajectory.get_reletive_speed())

    drawer.draw(cam)

    if time_coefficient[1]*time_coefficient[0] <1000:
        text1 = f1.render(str(time_coefficient[1]*time_coefficient[0])+"X", 1, (255,255,255))
    elif time_coefficient[1]*time_coefficient[0] <1000000:
        text1 = f1.render(str((time_coefficient[1]*time_coefficient[0])//1000)+"kX", 1, (255,255,255))
    elif time_coefficient[1]*time_coefficient[0] >=1000000:
        text1 = f1.render(str((time_coefficient[1]*time_coefficient[0])//1000000)+"MX", 1, (255,255,255))
    text2 = f1.render(str(round(thrust,2)), 1, (255,255,255))
    text3 = f2.render("управление: WASD - ракета, ",1,(255,255,255))
    text4 = f2.render("стрелки - камера, скролл - масштабирование, +/- время ",1,(255,255,255))
    text5 = f2.render("Цифры 1-8 - предустановленные длины траектории",1,(255,255,255))
    text6 = f2.render("u - добавить длину,i - убавить длину, o - замкнуть траекторию",1,(255,255,255))
    screen.blit(text1, (WW*2/100, WH/50))
    screen.blit(text2, (WW*98/100, WH/50))
    screen.blit(text3, (WW/100, WH*46/50))
    screen.blit(text4, (WW/100, WH*47/50))
    screen.blit(text5, (WW/100, WH*48/50))
    screen.blit(text6,(WW/100, WH*49/50))


    pg.display.update()
    clock.tick(150)
    




pg.quit()