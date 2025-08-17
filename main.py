import sys
import pygame
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(True)

pygame.init()
pygame.display.set_caption("Drawing Tool")
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
panel_width = 300
panel_padding = 10
scroll_offset = 0

objects.clear()

color_buttons = [
    ['Black', lambda: change_color([0, 0, 0])],
    ['White', lambda: change_color([255, 255, 255])],
    ['Red', lambda: change_color([255, 0, 0])],
    ['Blue', lambda: change_color([0, 0, 255])],
    ['Yellow', lambda: change_color([255, 255, 0])],
    ['Orange', lambda: change_color([255, 165, 0])],
    ['Green', lambda: change_color([0, 255, 0])],
    ['Light Blue', lambda: change_color([173, 216, 230])],
    ['Purple', lambda: change_color([105, 0, 198])],
]

title_colors = font.render("Colors", True, (230, 230, 230))
title_tools = font.render("Brushes", True, (230, 230, 230))
title_file = font.render("File", True, (230, 230, 230))

title_colors_y = panel_padding
start_y_colors = title_colors_y + title_colors.get_height() + 10

for index, button_name in enumerate(color_buttons):
    col = index % 2
    row = index // 2

    x = panel_padding + col * (button_width + panel_padding)
    y = start_y_colors + row * (button_height + panel_padding)

    Button(x, y, button_width, button_height,
           button_name[0], button_name[1])

last_color_row = (len(color_buttons) + 2) // 2
separator_y = start_y_colors + last_color_row * (button_height + panel_padding) + panel_padding

tool_buttons = [
    ['Brush Larger', lambda: change_brush_size('greater')],
    ['Brush Smaller', lambda: change_brush_size('smaller')],
]

title_tools_y = separator_y + 5
start_y_tools = title_tools_y + title_tools.get_height() + 10

for index, button_name in enumerate(tool_buttons):
    col = index % 2
    row = index // 2

    x = panel_padding + col * (button_width + panel_padding)
    y = start_y_tools + 20 + row * (button_height + panel_padding)

    Button(x, y, button_width, button_height, button_name[0], button_name[1])

last_tool_row = (len(tool_buttons) + 2) // 2
separator2_y = start_y_tools + last_tool_row * (button_height + panel_padding) + panel_padding

file_buttons = [
    ['Save', save]
]

title_file_y = separator2_y + panel_padding
start_y_file = title_file_y + title_file.get_height() + panel_padding

for index, button_name in enumerate(file_buttons):
    x = panel_padding
    y = start_y_file

    Button(x, y, panel_width - 2 * panel_padding, button_height, button_name[0], button_name[1])

canvas = pygame.Surface(canvas_size)
canvas.fill((255, 255, 255))

while True:
    screen.fill((30, 30, 30))
    x, y = screen.get_size()

    pygame.draw.rect(screen, (50, 50, 50), (0, 0, panel_width, y))

    screen.blit(title_colors, (panel_padding, title_colors_y))
    pygame.draw.line(screen, (200, 200, 200), (panel_padding, separator_y),
                     (panel_width - panel_padding, separator_y), 2)

    screen.blit(title_tools, (panel_padding, separator_y + 5))
    pygame.draw.line(screen, (200, 200, 200), (panel_padding, separator2_y),
                     (panel_width - panel_padding, separator2_y), 2)

    screen.blit(title_file, (panel_padding, separator2_y + 5))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    for obj in objects:
        obj.button_rect.y = obj.y + scroll_offset
        obj.process()

    screen.blit(canvas, [x / 2 - canvas_size[0] / 2, y / 2 - canvas_size[1] / 2])

    if pygame.mouse.get_pressed()[0]:
        mx, my = pygame.mouse.get_pos()
        dx = mx - x / 2 + canvas_size[0] / 2
        dy = my - y / 2 + canvas_size[1] / 2

        pygame.draw.circle(canvas, draw_color, [dx, dy], brush_size)

        if 0 <= dx < canvas_size[0] and 0 <= dy < canvas_size[1]:
            pygame.draw.circle(canvas, draw_color, [int(dx), int(dy)], brush_size)

    pygame.draw.circle(screen, draw_color, [panel_width * 5 - 50, 100], brush_size)

    pygame.display.flip()
    fps_clock.tick(fps)
