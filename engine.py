import tkinter as tk
from maths import *
from objects import Scene
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
        self.current_scene = None

        # Бинд нужных кнопок
        self.last_f11_press = 0
        self.fullscreen_mode = False
        self.bind_key("F11", self.switch_full_screen) # Переключение режима окна

        self.last_f3_press = 0
        self.debug_mode = False
        self.bind_key("F3", self.switch_debug_mode) # Переключение режима debug

    def turn_off(self):
        self.running = False

    def bind_key(self, key: str, func: callable):
        self.Window.bind(f"<{key}>", lambda e: func(e))

    def switch_full_screen(self, event):
        if time.perf_counter() - self.last_f11_press > 0.5:
            self.last_f11_press = time.perf_counter()
            self.fullscreen_mode = not(self.fullscreen_mode)
            self.Window.attributes('-fullscreen', self.fullscreen_mode)

    def switch_debug_mode(self, event):
        if time.perf_counter() - self.last_f3_press > 0.25:
            self.last_f3_press = time.perf_counter()
            self.debug_mode = not(self.debug_mode)

    def set_scene(self, scene: Scene):
        self.current_scene = scene

    def draw_debug_menu(self, current_fps: float):
        # Отрисовка меню Debug
        fps_label = self.canvas.create_text(70, 20, text=f"FPS: {clump(current_fps, 0, FPS)}", font=("Arial", 12), anchor="se", tag="fps_text")

        window_width = self.Window.winfo_width()
        window_height = self.Window.winfo_height()

        center = Pos2(window_width//2, window_height//2)
        radius = 5
        self.canvas.create_line(0, window_height//2, window_width, window_height//2, tag="width_line")
        self.canvas.create_line(window_width//2, 0, window_width//2, window_height, tag="height_line")
        self.canvas.create_oval(center.x - radius, center.y - radius, center.x + radius, center.y + radius, tag="center_oval")

    def destroy_debug_menu(self):
        self.canvas.delete("fps_text", "center_oval", "width_line", "height_line")

    def mainloop(self):
        while self.running:
            _delta1 = time.perf_counter() # Время начала кадра
            self.Window.update() # Обновление окна
            self.canvas.update()
            self.canvas.delete('all') # Очистка холста
            
            if self.current_scene != None:
                self.current_scene.render(self.canvas)

            render_delta = time.perf_counter() - _delta1 # Время рендеринга кадра

            if self.debug_mode:
                self.draw_debug_menu(current_fps=(int(1/render_delta)))
            self.Window.tksleep(DELTA - render_delta) # Простой в ожидании след кадра
        
        self.Window.destroy() # Выход из цикла отрисовки, завершение программы