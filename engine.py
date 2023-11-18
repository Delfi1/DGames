import tkinter as tk
from maths import Pos2, Size2, Rot2, FPS, Transform, DELTA, clump
from objects import Node, Camera2D
from gui import gui

import time
from multiprocessing import Process

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
        self.camera = Camera2D.default()
        
        # Создание доп параметров
        self.fullscreen_mode = False

        # Биндинг нужных кнопок
        self.last_f11_press = 0
        self.bind_key("F11", self.switch_full_screen) # Переключение режима окна

    def turn_off(self):
        self.running = False

    def bind_key(self, key: str, func: callable):
        self.Window.bind(f"<{key}>", lambda e: func(e))

    def sort_key(self, obj):
        return obj.layer

    def draw_gui(self):
        WTransorm = Transform(Pos2(0, 0), Size2(self.Window.winfo_width(), self.Window.winfo_height())) # Верхний левый угол

        for obj in self.gui_objects:
            obj.draw(self.canvas, WTransorm)

    # Функция рендеринга всех объектов
    def render_screen(self):
        for obj in self.objects:
            # obj.pos + screen_center() + camera.pos
            screen_center = Pos2(self.Window.winfo_width()//2, self.Window.winfo_height()//2)

            render_transform = obj.transform + Transform(screen_center) + self.camera.transform

            obj.render(self.canvas, render_transform)

    # Функция добавления объекта
    def add_object(self, *objs: Node):
        for obj in list(objs):
            if not(obj in self.objects):
                self.objects.append(obj)

    # Функция добавления объекта
    def add_gui(self, *objs: gui):
        for obj in list(objs):
            if not(obj in self.gui_objects):
                self.gui_objects.append(obj)

    def switch_full_screen(self, event):
        if time.perf_counter() - self.last_f11_press > 0.5:
            self.last_f11_press = time.perf_counter()
            self.fullscreen_mode = not(self.fullscreen_mode)
            self.Window.attributes('-fullscreen', self.fullscreen_mode)
    
    def debug_menu(self, current_fps: float):
        # Отрисовка меню Debug
        cam_pos_label = self.canvas.create_text(100, 20, text=f"Pos: {self.camera.transform.position}", font=("Arial", 12), anchor="se")
        fps_label = self.canvas.create_text(100, 40, text=f"FPS: {clump(current_fps, 0, FPS)}", font=("Arial", 12), anchor="se")

        window_width = self.Window.winfo_width()
        window_height = self.Window.winfo_height()

        center = Pos2(window_width//2, window_height//2)
        radius = 5
        self.canvas.create_line(0, window_height//2, window_width, window_height//2)
        self.canvas.create_line(window_width//2, 0, window_width//2, window_height)
        self.canvas.create_oval(center.x - radius, center.y - radius, center.x + radius, center.y + radius)

    def mainloop(self, _main: callable):
        while self.running:
            _delta1 = time.perf_counter() # Время начала кадра
            self.Window.update() # Обновление окна
            _main(self) # Выполнение основной функции

            # Сортировка всех объектов по layer (каждый кадр)
            self.objects.sort(key=self.sort_key)

            # Очистка холоста
            self.canvas.delete('all')

            # Отрисовка всего окна
            Process(target=self.render_screen).run()
            self.draw_gui()

            _delta2 = time.perf_counter() # Время конца кадра
            render_delta = _delta2 - _delta1
            self.debug_menu(current_fps=(int(1/render_delta)))
            self.Window.tksleep(DELTA - render_delta) # Простой в ожидании след кадра
        
        self.Window.destroy() # Выход из цикла отрисовки, завершение программы