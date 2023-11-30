"""Только в этом модуле можно предпринмать какие-то активные действия.
 Остальные модули по сути служат библиотекой, в них стараемся не писать ничего что не является функцией или классом"""

import pygame as pg
 
import deltaV_test
from deltaV_vis import *
from deltaV_library import*
#settings
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800

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

    TestObject = GameObject(100, 1E6, 1E3, 0, 2E6)
    

    gameStage = 1

while gameStage==1:
    #deltaV_test.testMain()
    screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    c = Drawable("circle",100,100,1,0xFF0000)
    cam = Camera()
    drawer = ScreenDrawer(screen)
    
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            gameStage="No"
        else:
            pass
        cam.move(event)
        drawer.draw(cam)
    pg.display.update()
    clock.tick(30)
    



pg.quit