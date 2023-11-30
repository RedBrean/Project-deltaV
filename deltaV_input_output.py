"""Тут работа с файлами уровня"""
from deltaV_library import*
from deltaV_physics import*
import deltaV_library

def read_level_from_file(file_name) -> list:
    """Читает из файла.
    Разделение "; ". 
    0 параметр тип объекта
    1-5 физические характеристики
    
    """
    with open(file_name) as input_file:
        objects = []
        for line in input_file:
            if len(line.strip()) == 0 or line[0] == '#':
                continue  # пустые строки и строки-комментарии пропускаем
            parametrs = line.split("; ")
            object_type = parametrs[0].lower()
            if object_type == "game_object": 
                new_object =  GameObject()
                new_object.parse_from_list(parametrs[1:6])
                objects.append(new_object)
        return objects