import time
import math

import pygame

from main.core.files.files import get_object_from_txt_file, var_from_dict

pygame.init()

# Customization
path = "Config\\customization.txt"
customization = get_object_from_txt_file(path, dict)
# System Font
font, customization = var_from_dict("system font", customization, path)
font_size, customization = var_from_dict("system font size", customization, path)
font = pygame.font.SysFont(font, font_size)
font_color, customization = var_from_dict("system text color", customization,
                                         path)
# Input Font
input_font, customization = var_from_dict("input font", customization, path)
input_font_size, customization = var_from_dict("input font size", customization,
                                               path)
input_font = pygame.font.SysFont(input_font, input_font_size)
input_font_color, customization = var_from_dict("input font color",
                                                customization,
                                                path)
# Application Colors
cursor_color, customization = var_from_dict("cursor color", customization, path)
border_color, customization = var_from_dict("border color", customization, path)
background_color, customization = var_from_dict("background color",
                                                customization, path)
scroll_color, customization = var_from_dict("scroll bar color",
                                            customization, path)

# Settings
path = "Config\\settings.txt"
settings = get_object_from_txt_file(path, dict)
cursor_blink, settings = var_from_dict("cursor blink", settings, path)
cursor_blink_rate, settings = var_from_dict("cursor blink rate", settings, path)
cursor_symbol, settings = var_from_dict("cursor symbol", settings, path)
cursor_centered, settings = var_from_dict("cursor centered", settings, path)
scroll_amount, settings = var_from_dict("scroll amount", settings, path)
dashes_enabled, settings = var_from_dict("dashes enabled", settings, path)

font_width, font_height = font.size(cursor_symbol)

# Layout
path = "Config\\layout_variables.txt"
layout_variables = get_object_from_txt_file(path, dict)
margin_size, layout_variables = var_from_dict("margin size", layout_variables,
                                              path)
hor_padding, layout_variables = var_from_dict("horizontal padding",
                                              layout_variables, path)
ver_padding, layout_variables = var_from_dict("vertical padding",
                                              layout_variables, path)


class Box(object):
    """Stores the coords of a rect in a variety of ways

    Relative coords evaluate the string given to determine each point.
    Keywords are substituted with screen values.
    Coords can be updated by giving new screen boundaries.

    Absolute Coords are hard values with x1, y1, x2, y2

    Rect Coords use the standard rectangle coordinate format with x, y, w, h
    """

    def __init__(self, filled=True, border_color=border_color,
                 background_color=background_color, border_size=1):
        self.filled = filled
        self.border_color = border_color
        self.background_color = background_color
        self.border_size = border_size
        self.x1 = None
        self.x2 = None
        self.y1 = None
        self.y2 = None
        self.w = None
        self.h = None
        self.relative_coords = None

    def render(self, display):
        if self.filled:
            pygame.draw.rect(display, self.background_color,
                             [self.x1, self.y1, self.w, self.h])
        pygame.draw.rect(display, self.border_color,
                         [self.x1, self.y1, self.w, self.h], self.border_size)
        return display

    def set_rect_coords(self, x1, y1, w, h):
        self.x1 = x1
        self.y1 = y1
        self.w = w
        self.h = h
        self.x2 = self.x1 + self.w
        self.y2 = self.y1 + self.h

    def set_absolute_coords(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.w = self.x2 - self.x1
        self.h = self.y2 - self.y1

    def get_rect_coords(self):
        return [self.x1, self.y1, self.w, self.h]

    def get_absolute_coords(self):
        return [self.x1, self.y1, self.x2, self.y2]

    def set_relative_coords(self, screen_boundaries, relative_coords):
        self.relative_coords = relative_coords
        absolute_coords = []
        for coord in self.relative_coords:
            n_coord = coord.replace("LEFT", str(screen_boundaries[0]))
            n_coord = n_coord.replace("TOP", str(screen_boundaries[1]))
            n_coord = n_coord.replace("RIGHT", str(screen_boundaries[2]))
            n_coord = n_coord.replace("BOTTOM", str(screen_boundaries[3]))
            n_coord = n_coord.replace("MARGIN", str(margin_size))
            absolute_coords.append(eval(n_coord))
        self.x1 = absolute_coords[0]
        self.y1 = absolute_coords[1]
        self.x2 = absolute_coords[2]
        self.y2 = absolute_coords[3]
        self.w = self.x2 - self.x1
        self.h = self.y2 - self.y1

    def update_relative_coords(self, screen_boundaries):
        if self.relative_coords is None:
            raise SystemError("This box is not relative")
        self.set_relative_coords(screen_boundaries, self.relative_coords)


class TextBox(Box):
    """A box which can display text. Inherits from Box"""

    def __init__(self, filled=True,
                 border_color=border_color, background_color=background_color,
                 border_size=1):
        Box.__init__(self, filled, border_color, background_color, border_size)
        # TODO: Archive old part of string.
        # TODO: Only load from file if scrolled back that far
        self.scroll_position = 0
        self.text = []
        self.hover_words = []
        self.name = None
        self.wrapped_lines = []
        self.rewrap = True
        self.is_dirty = True

    def render(self, display):
        """Blitz the text box to the given display"""

        self.hover_words = []
        display = Box.render(self, display)
        if type(self.text) != type(list()):
            raise SyntaxError("Text must be an array")
        if len(self.text) > 0:
            if self.rewrap:
                self.rewrap = False
                self.get_wrap_lines()

            # Not enough width for a single char
            if self.wrapped_lines is None:
                return display

            max_height = 0
            for line in self.wrapped_lines:
                if self.max_height_of_line(line) > max_height:
                    max_height = self.max_height_of_line(line)

            # Window must be tall enough for largest font used
            if self.h > max_height + ver_padding * font_height * 2:
                ver_letter_padding = ver_padding * font_height
                hor_letter_padding = hor_padding * font_width
                line_num = 0
                none_on_screen = True
                can_scroll_down = False
                for line in self.wrapped_lines:
                    word_pos = 0
                    y_pos = self.y1 + self.scroll_position \
                            + self.height_of_line(self.wrapped_lines,
                                                  line_num) + ver_letter_padding
                    if y_pos >= self.y1 + ver_letter_padding:
                        if y_pos <= self.y2 - self.max_height_of_line(
                                line) - ver_letter_padding:
                            for word in line:
                                text = word.get_font().render(word.text, 1,
                                                              word.color)
                                x_pos = self.x1 + hor_letter_padding + word_pos

                                word_pos += word.get_font().size(word.text)[0]
                                self.hover_words.append(
                                    {"x": x_pos, "y": y_pos,
                                     "w": word.get_font().size(word.text)[0],
                                     "word": word})
                                none_on_screen = False
                                display.blit(text, (x_pos, y_pos))
                        else:
                            can_scroll_down = True
                    line_num += 1
                if none_on_screen:
                    self.scroll_position += scroll_amount
                    display = self.render(display)
                if can_scroll_down:
                    display = self.display_scroll(display, "down")
                if self.scroll_position < 0:
                    display = self.display_scroll(display, "up")
        self.is_dirty = False
        return display

    def display_scroll(self, display,
                       dir):
        self.is_dirty = True
        if dir == "up":
            pygame.draw.rect(display, scroll_color,
                             [self.x1 + self.border_size, self.y1,
                              self.w - self.border_size * 2,
                              ver_padding * font_height / 2])
        if dir == "down":
            pygame.draw.rect(display, scroll_color,
                             [self.x1 + self.border_size,
                              self.y2 - ver_padding * font_height / 2,
                              self.w - self.border_size * 2,
                              ver_padding * font_height / 2])

        return display

    def scroll(self, direction):
        self.is_dirty = True
        if direction == "up":
            # Checked in render already (line_on_screen var)
            self.scroll_position -= scroll_amount
        elif direction == "down":
            if self.scroll_position <= ver_padding - scroll_amount:
                self.scroll_position += scroll_amount
        else:
            raise SyntaxError("Must be 'up' or 'down'")

    def get_text_from_line(self, line):
        """Strings text together from line"""

        line_text = ""
        for word in line:
            line_text += word.text
        return line_text

    def get_wrap_lines(self):
        lines = []
        line = []
        for int_text in self.text:
            new_line = False
            if "new line" in int_text.codes.keys():
                if self.word_can_fit(int_text, line):
                    line.append(int_text)
                    lines.append(line)
                    line = []
                    new_line = True
                else:
                    lines.append(line)
                    line = []
            if not new_line:
                if self.word_can_fit(int_text, line):
                    line.append(int_text)
                else:
                    for word in int_text.split_into_words():
                        line, lines = self.letters_to_line(word, line, lines)
                        if line is None:
                            self.wrapped_lines = None
                            return

        lines.append(line)
        self.wrapped_lines = lines
        self.is_dirty = True

    def letters_to_line(self, word, line, lines, prev="", count=0):
        if self.word_can_fit(word, line):
            if word.text != "" and word.text != " ":
                line.append(word)
        elif word.get_font().size(word.text)[
            0] > self.w - hor_padding * font_width * 2:
            letters = self.letters_can_fit(word.text,
                                           self.w - font_width * hor_padding * 2
                                           - self.length_of_line(line),
                                           word.get_font())
            word_letters = word.split_into_letters(len(letters))
            word1 = word_letters[0].text.rstrip()

            if dashes_enabled:
                if word1 == prev and count > 1:
                    # If have already tried twice. Font too large
                    return None, None
                elif len(word1) == 1:
                    word_letters[1].text = word1 + word_letters[1].text
                    word_letters[0].text = ""
                if word_letters[0].text.rstrip() != "":
                    word_letters[1].text = word_letters[0].text[-1:] \
                                           + word_letters[1].text
                    word_letters[0].text = word_letters[0].text[
                                           :-1].rstrip() + "-"
            line.append(word_letters[0])
            lines.append(line)
            line = []

            line, lines = self.letters_to_line(word_letters[1], line, lines,
                                               word1, count + 1)
            if line is None:
                return None, None
        else:
            if line != []:
                lines.append(line)
            line = [word]
        return line, lines

    def letters_can_fit(self, word, space, word_font):
        new_word = ""
        for letter in word:
            if word_font.size(new_word + letter)[0] > space:
                return new_word
            new_word += letter

    def word_can_fit(self, word, line):
        if self.length_of_line(line) + word.get_font().size(word.text)[0] + (
                        hor_padding * font_width * 2) < self.w:
            return True
        return False

    def length_of_line(self, line, num_chars=0):
        total_len = 0
        iterated_chars = 0
        for word in line:
            for char in word.text:
                total_len += word.get_font().size(char)[0]
                iterated_chars += 1
                if iterated_chars >= num_chars and num_chars != 0:
                    return total_len
        return total_len

    def height_of_line(self, lines, num_lines=None):
        if num_lines == 0:
            return 0
        total_height = 0
        iterated_lines = 0
        for line in lines:
            total_height += self.max_height_of_line(line)
            iterated_lines += 1
            if num_lines is not None and iterated_lines >= num_lines:
                return total_height

        return total_height

    def max_height_of_line(self, line, num_words=0):
        max_height = 0
        iterated_words = 0
        for word in line:
            word_font = word.get_font()
            if word_font.size(word.text)[1] > max_height:
                max_height = word_font.size(word.text)[1]
            iterated_words += 1
            if iterated_words >= num_words and num_words != 0:
                return max_height
        return max_height

    def get_hovered(self, mouse_pos):
        """Gets any word being hovered by the mouse"""

        for word in self.hover_words:
            line_height = self.max_height_of_line([word["word"]])
            if is_within_rect(mouse_pos,
                              [word["x"], word["y"], word["x"] + word["w"],
                               word["y"] + line_height]):
                return word["word"]
        return False

    def add_text(self, text, color=font_color, codes=None, hover=None):
        """Adds to the box's text"""

        if hover is None:
            hover = []
        if codes is None:
            codes = {}
        self.text.append(InteractiveText(text, color, codes, hover))
        self.rewrap = True
        self.is_dirty = True

    def set_text(self, text, color=font_color, codes=None, hover=None):
        """Sets the box's text"""

        if hover is None:
            hover = []
        if codes is None:
            codes = {}
        self.text = [(InteractiveText(text, color, codes, hover))]
        self.rewrap = True
        self.is_dirty = True

    def set_text_array(self, text_array):
        """Gives full access to self.text"""

        self.text = text_array
        self.rewrap = True
        self.is_dirty = True

    def update_relative_coords(self, screen_boundaries):
        Box.update_relative_coords(self, screen_boundaries)
        self.rewrap = True
        self.is_dirty = True

    def set_absolute_coords(self, x1, y1, x2, y2):
        Box.set_absolute_coords(self, x1, y1, x2, y2)
        self.rewrap = True
        self.is_dirty = True

    def set_rect_coords(self, x1, y1, w, h):
        Box.set_rect_coords(self, x1, y1, w, h)
        self.rewrap = True
        self.is_dirty = True


class InputBox(TextBox):
    """A box which can also render a cursor. Inherits from TextBox"""

    def __init__(self, filled=True,
                 border_color=border_color, background_color=background_color,
                 border_size=1):
        TextBox.__init__(self, filled, border_color,
                         background_color, border_size)
        self.cursor_blink_time = get_current_time_millis()
        self.cursor_shown = True
        self.old_cursor_pos = 0

    def render(self, display, cursor_pos=None):
        """Renders the box with a cursor and no interaction"""

        display = Box.render(self, display)
        hor_letter_padding = hor_padding * font_width
        text = input_font.render(self.get_text_from_line(self.text), 1,
                           input_font_color)
        x_pos = self.x1 + hor_letter_padding * 1.5 \
                + self.scroll_position
        y_pos = self.y1 + (self.h / 2
                           - self.max_height_of_line(self.text) / 2)
        display.blit(text, (x_pos, y_pos))

        if self.scroll_position < 0:
            display = self.display_scroll(display, "left")
        if self.length_of_line(
                self.text) + self.scroll_position > self.w \
                - hor_padding * font_width:
            display = self.display_scroll(display, "right")
        if cursor_pos is not None:
            display = self.render_cursor(display, cursor_pos)
        if self.scroll_position > 0:
            self.scroll_position -= scroll_amount
            display = self.render(display)
        if self.length_of_line(self.text) + self.scroll_position < 0:
            self.scroll_position += scroll_amount
            display = self.render(display)
        return display

    def display_scroll(self, display,
                       dir):
        if dir == "left":
            pygame.draw.rect(display, scroll_color,
                             [self.x1, self.y1 + self.border_size,
                              hor_padding * font_width / 2,
                              self.h - self.border_size * 2])
        if dir == "right":
            pygame.draw.rect(display, scroll_color,
                             [self.x2 - hor_padding * font_width / 2,
                              self.y1 + self.border_size,
                              hor_padding * font_width / 2,
                              self.h - self.border_size * 2])
        return display

    def scroll(self, direction):
        if direction == "down":
            self.scroll_position += scroll_amount
        elif direction == "up":
            self.scroll_position -= scroll_amount
        else:
            raise SyntaxError("Must be 'up' or 'down'")

    def render_cursor(self, display, cursor_pos,
                      move_cursor=False):
        """Renders the cursor when called"""

        # Flash the cursor
        if get_current_time_millis() >= self.cursor_blink_time \
                + cursor_blink_rate and cursor_blink:
            self.cursor_shown = not self.cursor_shown
            self.cursor_blink_time = get_current_time_millis()

        if self.old_cursor_pos != cursor_pos:
            self.cursor_blink_time = get_current_time_millis()
            self.cursor_shown = True

        self.old_cursor_pos = cursor_pos

        # Render the cursor
        if self.cursor_shown:
            cursor = font.render(cursor_symbol, 1, cursor_color)
            hor_letter_padding = hor_padding * font_width
            if len(self.get_text_from_line(self.text)) > 0:
                cursor_offset = 0
                if cursor_centered:
                    cursor_offset = font.size(cursor_symbol)[0] / 2
                if cursor_pos == 0:
                    abs_cursor_pos = -cursor_offset
                else:
                    abs_cursor_pos = self.length_of_line(self.text,
                                                         cursor_pos) \
                                     - cursor_offset
            else:
                abs_cursor_pos = 0
            x_pos = self.x1 + hor_letter_padding * 1.5 + \
                    abs_cursor_pos + self.scroll_position
            y_pos = (
                self.y1 + self.h / 2 - self.max_height_of_line(self.text) / 2)
            display.blit(cursor, (x_pos, y_pos))

            # Move scroll if cursor off screen
            if x_pos <= self.x1 + hor_letter_padding:
                self.scroll_position += scroll_amount
                display = self.render_cursor(display, cursor_pos, True)
            elif x_pos >= self.x2 - hor_letter_padding:
                self.scroll_position -= scroll_amount
                display = self.render_cursor(display, cursor_pos, True)
            if move_cursor:
                display = self.render(display)
        return display


class InteractiveText(object):
    """Stores and renders interactive text"""

    def __init__(self, text, color=None, codes=None, hover=None):
        self.hover = hover
        self.color = color
        self.text = text
        self.codes = codes
        if color is None:
            self.color = font_color
        if hover is None:
            self.hover = []
        if codes is None:
            self.codes = {}
        self.pos = None

    def split_into_words(self):
        words = []
        i = 0
        for word in self.text.split(" "):
            i += 1
            word_text = word
            if i != len(self.text.split(" ")):
                word_text += " "
            words.append(
                InteractiveText(word_text, self.color, self.codes, self.hover))
        return words

    def split_into_letters(self, length):
        length = math.floor(length)
        words = []
        words.append(
            InteractiveText(self.text[:length],
                            self.color, self.codes, self.hover))
        words.append(
            InteractiveText(self.text[length:],
                            self.color, self.codes, self.hover))
        return words

    def get_font(self):
        if "font" not in self.codes:
            word_font = font
            if "font name" in self.codes:
                word_font = pygame.font.SysFont(self.codes["font name"],
                                                font_size)
                if "font size" in self.codes:
                    word_font = pygame.font.SysFont(self.codes["font name"],
                                                    self.codes["font size"])
            self.codes["font"] = word_font
        return self.codes["font"]


def get_current_time_millis():
    """Returns the current time in milliseconds"""
    return int(round(time.time() * 1000))


def update_screen(display, screen_objects, cursor_pos, screen_bounds=None):
    for key in screen_objects.keys():
        if screen_bounds is not None:
            screen_objects[key].update_relative_coords(screen_bounds)
        if screen_objects[key].is_dirty:
            display = screen_objects[key].render(display)
    display = screen_objects["input box"].render_cursor(display, cursor_pos)
    return display


def is_within_rect(point, rect):
    if point[0] >= rect[0] and point[0] <= rect[2]:
        if point[1] >= rect[1] and point[1] <= rect[3]:
            return True
    return False
