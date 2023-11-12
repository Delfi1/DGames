from engine import *

# Cоздание основного окна
root = tk.Tk()

# Настройка окна
root.title("Game 1")
root.geometry("700x500")
root.resizable(False, False)

# Создание Canvas для отрисовки
Cnv = tk.Canvas(root)

# Создание основоного объекта игры
game = Game(root)

# Добавляем Canvas на экран
Cnv.pack(fill=tk.BOTH, expand=True)

def cube_draw_func(canvas: tk.Canvas, pos: Pos2):
    size = 50
    canvas.create_oval(pos.x -size/2, pos.y - size/2, size/2 - 1 + pos.x, size/2 - 1 + pos.y)
    canvas.create_rectangle(pos.x -size/2, pos.y - size/2, size/2 + pos.x, size/2 + pos.y)

rect1 = rectangle(Pos2(10, 10), Pos2(120, 30))

game.add_gui(rect1)

cube = PhysObject(Pos2(100, 100), cube_draw_func)
camera = Camera2D(Pos2(0, 0))

game.add_object(camera)

is_fullscreen = False
is_spawn = False

def can_spawn(event):
    global is_spawn
    is_spawn = not(is_spawn)

root.bind('<e>', lambda e:can_spawn(e))

# Что делать в кадре?
counter = 0
def main(_game: Game):
    global counter
    global is_spawn
    global is_fullscreen

    if is_spawn:
        new_cube = cube.clone()
        counter += 1
        new_cube.pos = Pos2(random.randint(-250, 250), 0)
        _game.add_object(new_cube)
        print(f"Всего объектов: {counter}")
    
    if keyboard.is_pressed('w'):
        camera.vec.y += 5
    if keyboard.is_pressed('s'):
        camera.vec.y -= 5
    if keyboard.is_pressed('a'):
        camera.vec.x += 5
    if keyboard.is_pressed('d'):
        camera.vec.x -= 5
    
    if keyboard.is_pressed("F11"):
        is_fullscreen = not(is_fullscreen)
        _game.root.attributes("-fullscreen", is_fullscreen)
    

# Создание основного цикла игры
game.mainloop(Cnv, main)