import threading
import os
import datetime

from main.game.contents.places import SpatialObject
from main.core.files.files import get_object_from_txt_file, var_from_dict
from main.core.gui.interface import InteractiveText as IT
from main.core.files.files import get_path, get_files_in_path

path = "Config\\customization.txt"
customization = get_object_from_txt_file(path, dict)
system_text_color, customization = var_from_dict("system text color",
                                                 customization, path)
system_date_color, customization = var_from_dict("system date color",
                                                 customization, path)
system_font, customization = var_from_dict("system font",
                                           customization, path)
system_font_size, customization = var_from_dict("system font size",
                                                customization, path)

system_codes = {"font name": system_font, "font size": system_font_size,
                "clickable": True}


# TODO: Pretty much, objects can be entered and actions can be preformed.
# TODO: Actions take turns, objects are stepped through to find actions.
# TODO: If an action requires a target, enter action and then object path.


class GameSave(object):
    def __init__(self):
        self.events_text_history = []
        self.command_path = ""
        self.universe = None
        self.player = None
        self.actions = []

    def gen_spawn_area(self):
        """Generates the object tree down to the point of spawn"""

        self.universe = SpatialObject("Universe", None, None, None)
        # TODO: Universe next character of alphabet after number of saves
        self.universe.gen_spawn()

    def get_actions_from_path(self):
        """Iterate through universe and player and
        return further paths or false"""
        pass

    def get_objects_from_path(self):
        """Iterate through universe and player and
        return further paths or false
        """
        pass

    def set_command_path(self, path):
        """If either action or object from path, set path"""
        pass

    def step_back(self, num):
        """Steps back in path num number of objects"""
        pass

    def set_action_choices(self):
        if self.command_path == "Saves":
            self.actions = get_saves()  # TODO: Finish

    def get_actions_choices(self):
        return self.actions


def get_input_string():
    from __main__ import get_input_string
    return get_input_string()


def set_input_string(text):
    from __main__ import set_input_string
    set_input_string(text)


def set_info_text(text):
    from __main__ import set_text
    set_text("info pane", [IT(text, system_text_color, system_codes, None)])


def set_text(text):
    from __main__ import set_text
    set_text("info pane", [IT(text, system_text_color, system_codes, None)])


def get_saves():
    saves = {}
    for file in get_files_in_path("Saves"):
        file_path = get_path() + "Saves\\" + file
        date = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
        saves[date] = file
    return saves


class GameEvents(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, daemon=True)

    def run(self):
        temp_game_save = GameSave()

        set_info_text("Welcome to The Ensuing Panic. Choose a save file.")
