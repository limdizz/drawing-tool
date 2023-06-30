import sys
import pygame
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(True)

pygame.init()
fps = 150
fps_clock = pygame.time.Clock()
width, height = 1600, 900
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
font = pygame.font.SysFont('Times', 20)

objects = []
draw_color = [0, 0, 0]
brush_size = 30
brush_size_steps = 3
canvas_size = [800, 800]


class Button:
    def __init__(self, x, y, width, height, button_text='Button', onclick_function=None, one_press=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclick_function = onclick_function
        self.one_press = one_press

        self.fill_colors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.button_surface = pygame.Surface((self.width, self.height))
        self.button_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.button_surf = font.render(button_text, True, (20, 20, 20))
        self.already_pressed = False
        objects.append(self)

    def process(self):
        mouse_pos = pygame.mouse.get_pos()
        self.button_surface.fill(self.fill_colors['normal'])
        if self.button_rect.collidepoint(mouse_pos):
            self.button_surface.fill(self.fill_colors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.button_surface.fill(self.fill_colors['pressed'])

                if self.one_press:
                    self.onclick_function()
                elif not self.already_pressed:
                    self.onclick_function()
                    self.already_pressed = True

            else:
                self.already_pressed = False

        self.button_surface.blit(self.button_surf,
                                 [self.button_rect.width / 2 - self.button_surf.get_rect().width / 2,
                                  self.button_rect.height / 2 - self.button_surf.get_rect().height / 2])
        screen.blit(self.button_surface, self.button_rect)


def change_color(color):
    global draw_color
    draw_color = color


def change_brush_size(direction):
    global brush_size
    if direction == 'greater':
        brush_size += brush_size_steps
    else:
        brush_size -= brush_size_steps


def save():
    pygame.image.save(canvas, "canvas.png")


button_width = 120
button_height = 35

buttons = [
    ['Black', lambda: change_color([0, 0, 0])],
    ['White', lambda: change_color([255, 255, 255])],
    ['Red', lambda: change_color([255, 0, 0])],
    ['Blue', lambda: change_color([0, 0, 255])],
    ['Yellow', lambda: change_color([255, 255, 0])],
    ['Orange', lambda: change_color([255, 165, 0])],
    ['Green', lambda: change_color([0, 255, 0])],
    ['Light blue', lambda: change_color([173, 216, 230])],
    ['Purple', lambda: change_color([105, 0, 198])],
    ['Brush Larger', lambda: change_brush_size('greater')],
    ['Brush Smaller', lambda: change_brush_size('smaller')],
    ['Save', save]
]

for index, button_name in enumerate(buttons):
    Button(index * (button_width + 10) + 10, 10, button_width, button_height,
           button_name[0], button_name[1])

canvas = pygame.Surface(canvas_size)
canvas.fill((255, 255, 255))

while True:
    screen.fill((30, 30, 30))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    for obj in objects:
        obj.process()

    x, y = screen.get_size()
    screen.blit(canvas, [x / 2 - canvas_size[0] / 2, y / 2 - canvas_size[1] / 2])

    if pygame.mouse.get_pressed()[0]:
        mx, my = pygame.mouse.get_pos()
        dx = mx - x / 2 + canvas_size[0] / 2
        dy = my - y / 2 + canvas_size[1] / 2
        pygame.draw.circle(canvas, draw_color, [dx, dy], brush_size)

    pygame.draw.circle(screen, draw_color, [100, 100], brush_size)
    pygame.display.flip()
    fps_clock.tick(fps)
