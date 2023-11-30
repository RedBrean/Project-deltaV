"""Только в этом модуле можно предпринмать какие-то активные действия.
 Остальные модули по сути служат библиотекой, в них стараемся не писать ничего что не является функцией или классом"""

import pygame as pg
 
import deltaV_test

from deltaV_vis import *
from deltaV_library import*
from deltaV_input_output import*
from deltaV_physics import*
#settings
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800

file_name = "solar_system.txt"

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

    cam = Camera()
    drawer = ScreenDrawer(screen)
    
    objects = read_level_from_file(file_name)
    
    mainPhisMod = PhysicalModulation(object)

    gameStage = 1

while gameStage==1:
    
    mainPhisMod.update_by_dt_few_times(10000, 100)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            gameStage="No"
        else:
            pass
        cam.move(event)
        drawer.draw(cam,objects)
    pg.display.update()
    clock.tick(30)
    



pg.quit()