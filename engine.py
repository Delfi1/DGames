import tkinter as tk
from maths import Pos2, FPS, DELTA
from objects import Node, Square

import time

# Создание функции sleep() для окна
def tksleep(self, time:float) -> None:
    self.after(int(time*1000), self.quit)
    self.mainloop()
tk.Misc.tksleep = tksleep

class Game():
    def __init__(
        self,
        title: str, geometry: str,
        resizable: bool
        ):
        # Настрока окна
        self.Window = tk.Tk()

        self.running = True

        self.Window.title(title)
        self.Window.geometry(geometry)
        self.Window.resizable(resizable, resizable)
        self.Window.protocol("WM_DELETE_WINDOW", self.turn_off) # Переключение работы игры

        # Создание холста
        self.canvas = tk.Canvas()
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Создание необходимых массивов
        self.objects = list()
        self.gui_objects = list()
        self.camera_pos = Pos2(0, 0)

    def turn_off(self):
        self.running = False

    # Функция рендеринга GUI
    def render_gui(self):
        for obj in self.gui_objects:
            obj.render()

    # Функция рендеринга всех объектов
    def render_screen(self):
        for obj in self.objects:
            # obj.pos + screen_center() + camera.pos
            screen_center = Pos2(self.Window.winfo_width()//2, self.Window.winfo_height()//2)

            render_pos = obj.pos + screen_center + self.camera_pos

            obj.render(self.canvas, render_pos)

    # Функция добавления объекта
    def add_object(self, *objs: Node):
        for obj in list(objs):
            if not(obj in self.objects):
                self.objects.append(obj)

    def mainloop(self, _main: callable):
        while self.running:
            _delta1 = time.perf_counter() # Время начала кадра
            self.Window.update() # Обновление окна
            _main(self)

            # Очистка холоста
            self.canvas.delete('all')

            # Отрисовка всего окна
            self.render_screen()
            #self.render_gui(self.canvas)

            _delta2 = time.perf_counter() # Время конца кадра
            render_delta = _delta2 - _delta1
            
            self.Window.tksleep(DELTA - render_delta) # Простой в ожидании след кадра
        
        self.Window.destroy() # Выход из цикла отрисовки, завершение программы