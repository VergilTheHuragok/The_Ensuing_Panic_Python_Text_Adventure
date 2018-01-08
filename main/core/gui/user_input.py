from main.core.files.files import get_object_from_txt_file, var_from_dict

path = "Config\\settings.txt"
settings = get_object_from_txt_file(path, dict)
key_tick, settings = var_from_dict("key tick", settings, path)
key_repeat_delay, settings = var_from_dict("key repeat delay", settings, path)
max_keys_pressed, settings = var_from_dict("max keys pressed", settings, path)
unshifted_keys, settings = var_from_dict("unshifted keys", settings, path)
shifted_keys, settings = var_from_dict("shifted keys", settings, path)

keys = {}
alphanumerals = "abcdefghijklmnopqrstuvwxyz1234567890"


def is_character(key):
    """Tests whether given key is a character.
    Used internally.

    :type key: str
    """

    if key in shifted_keys or key in unshifted_keys or key.lower() \
            in alphanumerals:
        return True
    return False


def press_key(key):
    """Acknowledges key press if it is the only key being pressed or if
    multiple_key_repeat is on
    """

    keys_pressed = 0
    if is_character(key):
        for key_to_check in keys.keys():
            if keys[key_to_check] > 0 and is_character(key_to_check):
                keys_pressed += 1
    if keys_pressed < max_keys_pressed:
        keys[key] = 1


def reset_key(key):
    keys.pop(key, None)


def shift_keys(string):
    nstring = ""
    for char in string:
        if char in unshifted_keys:
            nstring += shifted_keys[unshifted_keys.index(char)]
        else:
            nstring += char

    return nstring


def index_of_next_word(text, cursor_pos, direction="right"):
    if direction == "left":
        return text[:cursor_pos].rstrip(" ").rfind(" ")
    elif direction == "right":
        return text[cursor_pos:].lstrip(" ").find(" ") + len(
            text[:cursor_pos]) + 1


def backspace(input_string, cursor_pos, control):
    if control:
        if " " in input_string[:cursor_pos].rstrip(" "):
            inp_string_len = len(input_string)
            input_string = \
                input_string[:
                index_of_next_word(input_string,
                                   cursor_pos, "left")] \
                + " " \
                + input_string[cursor_pos:]
            cursor_pos -= (inp_string_len - len(input_string))
        else:
            input_string = input_string[cursor_pos:]
            cursor_pos = 0
    else:
        if cursor_pos != 0:
            input_string = input_string[:cursor_pos - 1] \
                           + input_string[cursor_pos:]
        cursor_pos -= 1
    return input_string, cursor_pos


def delete(input_string, cursor_pos, control):
    if control:
        if " " in input_string[cursor_pos:].lstrip(" "):
            input_string = input_string[:cursor_pos] + " " \
                           + input_string[
                             index_of_next_word(input_string,
                                                cursor_pos,
                                                "right"):] \
                               .lstrip(" ")
        else:
            input_string = input_string[:cursor_pos]
    else:
        if cursor_pos != len(input_string):
            input_string = input_string[:cursor_pos] \
                           + input_string[cursor_pos + 1:]
    return input_string, cursor_pos


def space(input_string, cursor_pos):
    input_string = input_string[:cursor_pos] \
                   + " " \
                   + input_string[cursor_pos:]
    cursor_pos += 1
    return input_string, cursor_pos


def left(input_string, cursor_pos, control):
    if control:
        if " " in input_string[:cursor_pos].rstrip(" "):
            cursor_pos = index_of_next_word(input_string,
                                            cursor_pos, "left")
        else:
            cursor_pos = 0
    else:
        cursor_pos -= 1
    return input_string, cursor_pos


def right(input_string, cursor_pos, control):
    if control:
        if " " in input_string[cursor_pos:].lstrip(" "):
            cursor_pos = index_of_next_word(input_string,
                                            cursor_pos, "right")
        else:
            cursor_pos = len(input_string)
    else:
        cursor_pos += 1
    return input_string, cursor_pos


def add_character(input_string, cursor_pos, shift, caps, key):
    cursor_pos += 1
    nkey = key

    if (shift):
        nkey = shift_keys(nkey)
    if caps != shift:
        nkey = nkey.upper()
        input_string = input_string[:cursor_pos - 1] \
                       + nkey \
                       + input_string[cursor_pos - 1:]
    else:
        input_string = input_string[:cursor_pos - 1] \
                       + nkey \
                       + input_string[cursor_pos - 1:]
    return input_string, cursor_pos


def typing(input_string, cursor_pos=-1):
    shift = ("left shift" in keys or "right shift" in keys)
    caps = ("caps lock" in keys)
    control = ("left ctrl" in keys or "right ctrl" in keys)
    for key in keys.keys():
        if (keys[key] > key_repeat_delay and keys[key] % key_tick == 0) \
                or (keys[key] == 1):

            if key == "backspace":
                input_string, cursor_pos = backspace(input_string, cursor_pos,
                                                     control)
            elif key == "delete":
                input_string, cursor_pos = delete(input_string, cursor_pos,
                                                  control)
            elif key == "space":
                input_string, cursor_pos = space(input_string, cursor_pos)
                # TODO: Only space if valid path
            elif key == "return":
                return input_string, True, 0
                # TODO: Only return if valid command
            elif key == "left":
                input_string, cursor_pos = left(input_string, cursor_pos,
                                                control)
            elif key == "right":
                input_string, cursor_pos = right(input_string, cursor_pos,
                                                 control)
            elif len(key) < 2:  # A standard character was pressed
                input_string, cursor_pos = add_character(input_string, cursor_pos,
                                                     shift, caps, key)

        if keys[key] > 0:
            keys[key] += 1
        if cursor_pos < 0:
            cursor_pos = 0
        if cursor_pos > len(input_string):
            cursor_pos = len(input_string)

    return input_string, False, cursor_pos
