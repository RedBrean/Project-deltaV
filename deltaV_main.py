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
   
    
    objects = read_level_from_file(file_name)
    drawer = ScreenDrawer(screen,objects)

    cam = Camera()
    cam.set_up_defoult(objects)

    mainPhisMod = PhysicalModulation(objects)

    #cam.SetPivot(objects[3])

    gameStage = 1

while gameStage==1:
    
    mainPhisMod.update_by_dt_few_times(100, 100)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            gameStage="No"
        elif event.type == pg.KEYDOWN:
            cam.move_by_key(event)
        elif event.type == pg.MOUSEBUTTONDOWN:
            button.try_pressing(event)
        elif event.type == pg.KEYUP:
            cam.move_by_key(event)
        else:
            pass
        cam.Scale(event)
    cam.Update()

    drawer.draw(cam)
    pg.display.update()
    clock.tick(60)
    



pg.quit()