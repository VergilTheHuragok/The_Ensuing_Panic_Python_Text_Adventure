import threading
import random

import pygame

import main.core.gui.user_input as ui
from main.core.files.files import get_object_from_txt_file, var_from_dict
from main.core.gui.interface import TextBox, InputBox, update_screen, is_within_rect
from main.game.start import GameEvents
from main.core.gui.interface import InteractiveText as IT


def set_text(box, text):
    """Takes a text array"""
    global screen_objects
    global SCREEN_LOCK
    global info_pane_text

    SCREEN_LOCK.acquire()
    if box == "info pane":
        info_pane_text = text
    else:
        screen_objects[box].set_text_array(text)
    SCREEN_LOCK.release()


def set_input_string(text):
    """Takes a text array"""
    global input_string
    global STRING_LOCK

    STRING_LOCK.acquire()
    input_string = text
    STRING_LOCK.release()


def get_input_string():
    global input_string
    global STRING_LOCK

    STRING_LOCK.acquire()
    string = input_string
    STRING_LOCK.release()
    return string


# File variables
path = "Config\\settings.txt"
settings = get_object_from_txt_file(path, dict)
pygame_fps, settings = var_from_dict("fps", settings, path)
screen_size, settings = var_from_dict("screen size", settings, path)

path = "Config\\window_layout.txt"
window_layout = get_object_from_txt_file(path, dict)

path = "Config\\customization.txt"
customization = get_object_from_txt_file(path, dict)
input_font, customization = var_from_dict("input font", customization, path)
input_font_color, customization = var_from_dict("input font color",
                                                customization, path)
input_font_size, customization = var_from_dict("input font size",
                                               customization,
                                               path)
temp_font_size, customization = var_from_dict("temp font size", customization,
                                              path)
# Multithreading variables
SCREEN_LOCK = threading.Lock()
STRING_LOCK = threading.Lock()

# Pygame Setup
pygame.init()
display = pygame.display.set_mode(screen_size, pygame.RESIZABLE)
pygame.display.set_caption("The Ensuing Panic")
pygame_clock = pygame.time.Clock()

# Window setup
screen_bounds = [0, 0, screen_size[0], screen_size[1]]
screen_objects = {}
info_pane_text = []

# Take boxes listed in config and create TextBoxes/InputBoxes
for window_box in window_layout.keys():
    if window_box == "input box":
        screen_objects[window_box] = InputBox(screen_bounds)
    else:
        screen_objects[window_box] = TextBox(screen_bounds)
    screen_objects[window_box].set_relative_coords(screen_bounds,
                                                   window_layout[window_box])
    screen_objects[window_box].name = window_box
    display = screen_objects[window_box].render(display)


# Input Vars
input_string = ""
returned = False
cursor_pos = 0
left_mouse_pressed = False
right_mouse_pressed = False
left_click = False
right_click = False

# Screen vars
hovering = False

game_events_loop = GameEvents()
game_events_loop.start()

# Main Event Loop
while True:

    # Screen Events
    pygame.event.pump()
    event = pygame.event.poll()

    # Tool bar options
    if event.type == pygame.QUIT:
        pygame.display.quit()
        print("QUITING")
        break
    if event.type == pygame.VIDEORESIZE:
        screen_size = event.dict['size']
        display = pygame.display.set_mode(screen_size, pygame.RESIZABLE)
        screen_bounds = [0, 0, screen_size[0], screen_size[1]]
        SCREEN_LOCK.acquire()
        display = update_screen(display, screen_objects,
                                cursor_pos, screen_bounds)
        SCREEN_LOCK.release()

    # User Input
    if event.type == pygame.KEYDOWN:
        ui.press_key(pygame.key.name(event.key))
    if event.type == pygame.KEYUP:
        ui.reset_key(pygame.key.name(event.key))
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 4:  # TODO: Page up/down scrolls with dir*10
            # TODO: or something
            # TODO: Home/End Move to home/end of text
            # TODO: Convert these to functions. DRY
            SCREEN_LOCK.acquire()
            if not hovering:
                for key in screen_objects.keys():
                    if is_within_rect(pygame.mouse.get_pos(),
                                      screen_objects[
                                          key].get_absolute_coords()):
                        window = key
                        break
            else:
                window = "info pane"
            screen_objects[window].scroll("down")
            SCREEN_LOCK.release()

        elif event.button == 5:
            SCREEN_LOCK.acquire()
            if not hovering:
                for key in screen_objects.keys():
                    if is_within_rect(pygame.mouse.get_pos(),
                                      screen_objects[
                                          key].get_absolute_coords()):
                        window = key
                        break
            else:
                window = "info pane"
            screen_objects[window].scroll("up")
            SCREEN_LOCK.release()

    # Mouse Presses
    if pygame.mouse.get_pressed()[0] and not left_mouse_pressed:
        left_mouse_pressed = True
        left_click = True
    else:
        left_click = False
    if not pygame.mouse.get_pressed()[0]:
        left_mouse_pressed = False

    if pygame.mouse.get_pressed()[2] and not right_mouse_pressed:
        right_mouse_pressed = True
        right_click = True
    else:
        right_click = False
    if not pygame.mouse.get_pressed()[2]:
        right_mouse_pressed = False

    # Set hover text
    hovering = False
    SCREEN_LOCK.acquire()
    for window in screen_objects.keys():
        if window != "input box":
            hover = screen_objects[window].get_hovered(
                pygame.mouse.get_pos())
            if hover:
                if hover.hover != []:
                    hovering = True
                    screen_objects["info pane"].set_text_array(hover.hover)
                    display = screen_objects["info pane"].render(display)
                if "clickable" in hover.codes:
                    STRING_LOCK.acquire()
                    if left_click:
                        input_string += hover.text
                        cursor_pos = len(input_string)
                    elif right_click:
                        input_string += hover.text
                        returned = True
                    STRING_LOCK.release()
                break
    if not hovering:
        screen_objects["info pane"].set_text_array(info_pane_text)
    SCREEN_LOCK.release()

    STRING_LOCK.acquire()
    input_string, n_returned, cursor_pos = ui.typing(
        input_string, cursor_pos)
    STRING_LOCK.release()

    if returned or n_returned:
        returned = True

    STRING_LOCK.acquire()
    SCREEN_LOCK.acquire()
    # TODO: Make command pathing
    codes = {"font name": input_font, "font size": input_font_size}
    screen_objects["input box"].set_text(input_string, input_font_color, codes,
                                         None)
    STRING_LOCK.release()
    SCREEN_LOCK.release()

    STRING_LOCK.acquire()
    if returned:  # TODO: Fix repeat returns
        print("Returned: " + input_string)
        returned_string = input_string
        input_string = ""
        returned = False
    STRING_LOCK.release()

    # Update Display
    SCREEN_LOCK.acquire()
    display = update_screen(display, screen_objects, cursor_pos, screen_bounds)
    SCREEN_LOCK.release()
    pygame_clock.tick(pygame_fps)
    pygame.display.flip()
