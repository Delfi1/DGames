from GUI import gui_obj, screen_center, rectangle
from objects import GameObject, Camera2D
from matrix import *
from maths import get_delta
from constants import FPS, DELTA

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

        # Добавляем параметры
        self.is_fullscreen = False
        self.debug_mode = True

    def add_object(self, *objs: GameObject):
        for obj in list(objs):
            if not(obj in self.objects):
                if obj._type() == "Camera2D" and self.find_camera(self.objects) != None:
                    self.objects.remove(self.find_camera(self.objects))
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
        if keyboard.is_pressed("F3"):
            self.debug_mode = not(self.debug_mode)
            print(f"Debug mode: {self.debug_mode}")
        if keyboard.is_pressed("F11"):
            self.is_fullscreen = not(self.is_fullscreen)
            self.root.attributes("-fullscreen", self.is_fullscreen)

    def debug_menu(self, fps):
        debug_rect = rectangle(Pos4(2, 2, 302, 152), color="grey", border=1)
        debug_rect.add_child()

        debug_rect.draw(self.game_canvas)

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
                        if self.debug_mode:
                            obj.render(self.game_canvas, screen_center(self.root))
                        continue
                    
                    render_pos = obj.pos + screen_center(self.root) + current_camera.pos

                    obj.render(self.game_canvas, render_pos)

                render_time = get_delta(start_)

                if self.debug_mode:
                    cur_fps = 1/render_time
                    self.debug_menu(fps=cur_fps)

                self.root.tksleep(DELTA - render_time) # Ожидание 
    
        except tk.TclError as e:
            print(e)
            print("Window is closed. Exiting...")