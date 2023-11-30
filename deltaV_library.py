"""модуль в котором класссы всякой мелочевки"""
from deltaV_vis import*
from deltaV_physics import*

class GameObject(SpaceObject, Drawable):
    def __init__(self, x: float = 0, y: float = 0, vx: float = 0, vy: float = 0, m: float = 0) -> None:
        SpaceObject.__init__(x, y, vx, vy, m)
        Drawable.__init__()


class Button():
    """Класс кнопки"""
    def __init__(self):
        pass

