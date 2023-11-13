from GUI import gui_obj, screen_center
from objects import GameObject, Camera2D
from matrix import Pos2, Vec2
from maths import get_delta
from constants import FPS

import time
import keyboard
import random
import tkinter as tk

def tksleep(self, time:float) -> None:
    self.after(int(time*1000), self.quit)
    self.mainloop()
tk.Misc.tksleep = tksleep

class Game():
    def __init__(self, title: str, geometry: str, resizable: bool):
        self.objects = []
        self.guis = []
        
        self.root = tk.Tk() # Cоздание основного окна
        
        # Настройка окна
        self.root.title(title)
        self.root.geometry(geometry)
        self.root.resizable(resizable, resizable)

        # Создание Canvas для отрисовки
        self.game_canvas = tk.Canvas(self.root)

        # Добавляем Canvas на экран
        self.game_canvas.pack(fill=tk.BOTH, expand=True)

    def add_object(self, *objs: GameObject):
        for obj in list(objs):
            if not(obj in self.objects):
                self.objects.append(obj)

    def add_gui(self, *guis: gui_obj):
        for g in list(guis):
            if not(g in self.guis):
                self.guis.append(g)
    
    def find_camera(self, objects: list) -> Camera2D | None:
        for obj in list(objects):
            if obj._type() == "Camera2D":
                return obj
        return None
    
    def key_pressing(self):
        if keyboard.is_pressed("F11"):
            self.root.attributes("-fullscreen", not(root.cget("-fullscreen")))

    def mainloop(self, _main: callable):
        try:
            while True:
                start_ = time.perf_counter()
                _main(self) # Вызываем необходимые функции

                self.key_pressing() # Проверка на нажатие клавиш

                self.root.update() # Обновление Окна

                # Очистка Canvas
                self.game_canvas.delete('all')

                current_camera = self.find_camera(self.objects)

                # Отрисовка gui объектов
                for g in self.guis:
                    g.draw(self.game_canvas)

                # Отрисовка всех объектов на экране
                for obj in self.objects:
                    if current_camera == None:
                        continue
                    # Отрисовка камеры, если нужно
                    if obj == current_camera:
                        #obj.draw(self.game_canvas, screen_center(self.root))
                        continue
                    
                    render_pos = obj.pos + screen_center(self.root) + current_camera.pos

                    obj.render(self.game_canvas, get_delta(start_), render_pos)
                self.root.tksleep(get_delta(start_)) # Ожидание 
    
        except tk.TclError:
            print("Window is closed. Exiting...")