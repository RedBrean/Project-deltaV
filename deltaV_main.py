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
    pg.font.init()
    f1 = pg.font.Font(None, 36)



    time_coefficients = [0.01, 0.1, 0.25, 0.5, 1, 2, 10, 25, 100, 250, 1000]
    time_coefficient_number = 4
    time_coefficient = time_coefficients[time_coefficient_number]
    
 
    
    objects = read_level_from_file(file_name)
    drawer = ScreenDrawer(screen,objects)

    cam = Camera()
    cam.set_up_defoult(objects)

    mainPhisMod = PhysicalModulation(objects)

    trajectory = Trajectory(objects, objects[3], objects[0], needAutoOptimization=True, k_Tsim=1.1)

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
    
    player = None
    for cObject in objects:
        if isinstance(cObject, Player):
            player = cObject
            break
    if(player == None):
        print("Нет игрока!")

    gameStage = 1


while gameStage==1: 

    time_coefficient = time_coefficients[time_coefficient_number]
    
    mainPhisMod.update_by_dt_few_times(100*time_coefficient, 100)
    
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
                if time_coefficient_number>1:
                    time_coefficient_number-=1
            if event.key == pg.K_1:
                time_coefficient_number=4
        elif event.type == pg.KEYUP:
            cam.move_by_key(event)
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

    trajectory.Update(50)

    drawer.draw(cam)

    text1 = f1.render(str(time_coefficients[time_coefficient_number])+"X", 1, (255,255,255))
    screen.blit(text1, (20, 60))

    pg.display.update()
    clock.tick(150)
    




pg.quit()