import os
from os import listdir
from os.path import isfile, join

from main.core.tools.python_console_tools import warning_print
from main.core.config.config import *  # DO NOT REMOVE


def is_compiled():
    """Checks whether the code is being ran from the exe or not"""

    if (r"C:\Users\Reece\floobits\share\Reece\The_Ensuing_Panic"
        r"\The_Ensuing_Panic_" in os.getcwd()):  # TODO: Always return True in
        # final verion?
        return False
    return True


def get_path():
    """Returns the path to the root of the game folder depending on
    is_compiled()
    """

    if is_compiled():
        return "..\\"
    else:
        return "C:\\Users\\Reece\\Desktop\\The Ensuing Panic\\"


def is_folder(folder, has_root=False):
    """Checks whether given path is a folder off the root of the game folder."""

    if os.path.isdir(get_path() + folder if not has_root else folder):
        return True
    return False


def is_file(path, has_root=False):
    """Checks whether given path is a file off the root of the game folder."""

    if os.path.exists(get_path() + path if not has_root else path):
        return True
    return False


def get_files_in_path(path, has_root=False):
    """Credit: http://stackoverflow.com/questions/
    3207219/how-to-list-all-files-of-a-directory
    """

    if has_root:
        n_path = path
    else:
        n_path = get_path() + path
    return [f for f in listdir(n_path) if isfile(join(n_path, f))]


def restore_default(default_path):
    """Restores specified files to defaults. Returns new file."""

    path_splice = get_path()
    default_path_parts = default_path.split("\\")
    new_file = eval(default_path_parts[-1][:-4])
    for path_part in default_path_parts:
        path_splice += path_part
        if not path_splice.endswith(".txt") and not is_folder(path_splice,
                                                              True):
            warning_print("Creating folder: " + path_splice)
            os.mkdir(path_splice)
        elif path_splice.endswith(".txt"):
            warning_print("Creating file: " + path_splice)
            if is_file(path_splice, True):
                os.remove(path_splice)
            file = open(path_splice, "w")
            file.write(new_file)
            file.close()
        path_splice += "\\"
    default = open(get_path() + default_path, "r")
    default_string = default.read()
    default.close()
    return eval(default_string)


def get_file_name(path):
    """Converts file path to file name"""

    file_name = path.split("\\")
    file_name = file_name[len(file_name) - 1]
    file_name = file_name[:-len(".txt")]
    file_name = file_name.title()
    file_name += " file"
    return file_name


def get_object_from_txt_file(path, object_type, redo=False):
    """Gets and object from a txt file.
    Handles any corrupt and missing files.
    """

    file_name = get_file_name(path)

    # Checking if config exists
    if is_file(path):
        txt_file = open(get_path() + path, "r")
        found_object = txt_file.read()
        txt_file.close()
        corrupt = False
        try:
            found_object = eval(found_object)
        except SyntaxError:
            corrupt = True
        if type(found_object) is not object_type or corrupt:
            warning_print(file_name + " is corrupted. Restoring to default.")
            os.remove(get_path() + path)

            # Trying Defaults
            return get_object_from_txt_file(path, object_type, True)
        # Success
        return found_object

    # Does not exist. Creating new config
    else:
        if not redo:
            warning_print(file_name + " is missing. Restoring to default.")
        found_object = restore_default(path)
        return found_object


def var_from_dict(var_name, _dict, path):
    """Takes the name of a variable, its config object, and the config's path.
    If the var_name is in the config, it is returned with the original object.
    Otherwise, the file is restored and the new var is returned with a new
    config object.
    """

    try:
        return _dict[var_name], _dict
    except KeyError:
        warning_print(
            get_file_name(
                path) + " is missing " + var_name + ". Restoring to default.")
        restore_default(path)
        _dict = get_object_from_txt_file(path, dict)
        return _dict[var_name], _dict
