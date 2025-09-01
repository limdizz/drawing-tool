import sys
import ctypes
import os
import pygame

ctypes.windll.shcore.SetProcessDpiAwareness(True)

pygame.init()
pygame.display.set_caption("Drawing Tool")
fps = 150
fps_clock = pygame.time.Clock()
width, height = 1600, 900
screen = pygame.display.set_mode((width, height))
font = pygame.font.SysFont('Times', 20)

objects = []
draw_color = [0, 0, 0]
brush_size = 30
brush_size_steps = 3
canvas_size = [800, 800]

button_width = 120
button_height = 35
panel_width = 300
panel_padding = 10
panel_visible = True
min_panel_width = 50
panel_target_width = 300
panel_speed = 15
toggle_button_rect = pygame.Rect(0, 0, 20, 60)

palette_width = 243
palette_height = 256
palette_x = panel_width - 285
palette_y = 600

show_palette = False
palette_close_btn = None


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


def choose_color():
    global show_palette
    show_palette = not show_palette


def draw_color_palette():
    global palette_close_btn, draw_color

    if not show_palette:
        return None

    pygame.draw.rect(screen, (100, 100, 100), (palette_x - 5, palette_y - 5, palette_width + 10, palette_height + 50),
                     border_radius=5)
    pygame.draw.rect(screen, (40, 40, 40), (palette_x, palette_y, palette_width, palette_height + 40), border_radius=5)

    for x in range(palette_width):
        for y in range(palette_height):
            r = x
            g = y
            b = 128
            screen.set_at((palette_x + x, palette_y + y), (r, g, b))

    palette_close_btn = pygame.Rect(palette_x + palette_width // 2 - 40, palette_y + palette_height + 10, 80, 30)
    pygame.draw.rect(screen, (200, 50, 50), palette_close_btn, border_radius=3)
    font_small = pygame.font.SysFont('Consolas', 18)
    text = font_small.render("Close", True, (255, 255, 255))
    screen.blit(text, (palette_close_btn.x + 15, palette_close_btn.y + 5))

    return palette_close_btn


def change_color(color):
    global draw_color
    draw_color = color


def change_brush_size(direction):
    global brush_size

    if direction == 'greater':
        brush_size += brush_size_steps
    else:
        brush_size -= brush_size_steps


last_save_path = None


def save():
    global last_save_path

    if last_save_path:
        pygame.image.save(canvas, last_save_path)
        show_save_message(f"Saved to {os.path.basename(last_save_path)}")
    else:
        save_as()


def save_as():
    global last_save_path

    filename = ""
    show_save_message("Enter filename in console")

    if not filename:
        print("Enter filename (with .png extension):")
        filename = input().strip()

    if not filename.endswith('.png'):
        filename += '.png'

    pygame.image.save(canvas, filename)
    last_save_path = filename
    show_save_message(f"Saved as {filename}")
    print(f"Saved as {filename}")


def show_save_message(text):
    font = pygame.font.SysFont("Arial", 18)
    message = font.render(text, True, (0, 200, 0))
    screen.blit(message, (panel_width + 20, 20))
    pygame.display.flip()
    pygame.time.delay(1500)


def save_canvas_state():
    if len(canvas_states) >= MAX_UNDO_STEPS:
        canvas_states.pop(0)
    canvas_states.append(canvas.copy())


def undo_action():
    if len(canvas_states) > 1:
        canvas_states.pop()
        canvas.blit(canvas_states.pop(), (0, 0))
    else:
        canvas.fill((255, 255, 255))
        if canvas_states:
            canvas_states[0] = canvas.copy()


objects.clear()

title_colors = font.render("Colors", True, (230, 230, 230))
title_tools = font.render("Brushes", True, (230, 230, 230))
title_file = font.render("File", True, (230, 230, 230))

title_colors_y = panel_padding
start_y_colors = title_colors_y + title_colors.get_height() + panel_padding
Button(panel_padding, start_y_colors, button_width * 2 + panel_padding, button_height, "Choose Color", choose_color)

separator_y = start_y_colors + button_height + panel_padding

tool_buttons = [
    ['Brush +', lambda: change_brush_size('greater')],
    ['Brush -', lambda: change_brush_size('smaller')],
]

title_tools_y = separator_y + panel_padding
start_y_tools = title_tools_y + title_tools.get_height() + panel_padding

for index, button_name in enumerate(tool_buttons):
    col = index % 2
    row = index // 2

    x = panel_padding + col * (button_width + panel_padding)
    y = start_y_tools + row * (button_height + panel_padding)

    Button(x, y, button_width, button_height, button_name[0], button_name[1])

last_tool_row = (len(tool_buttons) + 1) // 2
separator2_y = start_y_tools + last_tool_row * (button_height + panel_padding) + panel_padding

file_buttons = [
    ['Save', save],
    ['Save As...', save_as],
    ['Undo', undo_action],
]

title_file_y = separator2_y + panel_padding
start_y_file = title_file_y + title_file.get_height() + panel_padding

for index, button_name in enumerate(file_buttons):
    col = index % 2
    row = index // 2
    x = panel_padding + col * (button_width + panel_padding)
    y = start_y_file + row * (button_height + panel_padding)

    Button(x, y, button_width, button_height, button_name[0], button_name[1])

canvas = pygame.Surface(canvas_size)
canvas.fill((255, 255, 255))
canvas_states = []
MAX_UNDO_STEPS = 50
save_canvas_state()

fullscreen = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((width, height))
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if show_palette:
                mouse_pos = pygame.mouse.get_pos()

                if (palette_x <= mouse_pos[0] <= palette_x + 256 and
                        palette_y <= mouse_pos[1] <= palette_y + 256):
                    rel_x = mouse_pos[0] - palette_x
                    rel_y = mouse_pos[1] - palette_y
                    draw_color = [rel_x, rel_y, 128]

                if palette_close_btn and palette_close_btn.collidepoint(mouse_pos):
                    show_palette = False

    screen.fill((30, 30, 30))

    x, y = screen.get_size()
    screen.blit(canvas, [x / 2 - canvas_size[0] / 2, y / 2 - canvas_size[1] / 2])
    pygame.draw.rect(screen, (50, 50, 50), (0, 0, panel_width, y))
    screen.blit(title_colors, (panel_padding, title_colors_y))

    pygame.draw.line(screen, (200, 200, 200), (panel_padding, separator_y),
                     (panel_width - panel_padding, separator_y), 2)

    screen.blit(title_tools, (panel_padding, separator_y + 5))
    pygame.draw.line(screen, (200, 200, 200), (panel_padding, separator2_y),
                     (panel_width - panel_padding, separator2_y), 2)

    screen.blit(title_file, (panel_padding, separator2_y + 5))

    for obj in objects:
        obj.process()

    if show_palette:
        draw_color_palette()

    if pygame.mouse.get_pressed()[0] and (not show_palette or
                                          not (panel_width + 50 <= pygame.mouse.get_pos()[
                                              0] <= panel_width + 50 + 256 and
                                               50 <= pygame.mouse.get_pos()[1] <= 50 + 256)):
        mx, my = pygame.mouse.get_pos()
        dx = mx - x / 2 + canvas_size[0] / 2
        dy = my - y / 2 + canvas_size[1] / 2

        if 0 <= dx < canvas_size[0] and 0 <= dy < canvas_size[1]:
            if not canvas_states or canvas_states[-1].get_at((int(dx), int(dy))) != canvas.get_at((int(dx), int(dy))):
                save_canvas_state()
            pygame.draw.circle(canvas, draw_color, [int(dx), int(dy)], brush_size)

    pygame.draw.circle(screen, draw_color, [panel_width * 5 - 50, 100], brush_size)

    pygame.display.flip()
    fps_clock.tick(fps)
