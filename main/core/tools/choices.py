from core.files.files import get_object_from_txt_file

abbreviations = None


def get_abbreviations():
    """Returns the abbreviation list. If it is None, this regens it.
    """

    global abbreviations

    if abbreviations is None:
        abbreviations = get_object_from_txt_file("config\\abbreviations.txt",
                                                 dict)
    return abbreviations


def get_keys_from_value(value, _dict, case_sensitive=False):
    """Returns list of keys in dict with value given"""

    matching_keys = []
    for key in _dict.keys():
        for val in _dict.get(key):
            if not case_sensitive:
                if value.lower() == val.lower():
                    matching_keys.append(key)
            else:
                if value == val:
                    matching_keys.append(key)
    return matching_keys


def display_choices(choices):
    print(choices)


def choice_from_list(choices, hidden_choices=["list"]):
    """Takes a list of choices and returns the choice the user picks.
    Also checks abbreviations.
    """

    if "list" not in hidden_choices:
        hidden_choices.append("list")

    # Do not want any case-sensitivity
    choices = [x.lower() for x in choices]
    hidden_choices = [x.lower() for x in hidden_choices]

    abbreviations = get_abbreviations()
    input_string = "\nChoose an option or type \"list\" " \
                   "for available choices: "
    # A "" in hidden_choices means the choices have been limited due to
    # abbreviation conflict
    if "" in hidden_choices:
        input_string = "\nChoose an option, type \"list\" " \
                       "for available choices, or leave blank " \
                       "to return to all choices: "
    user_input = input(input_string).lower()

    # User inputted an existing choice
    if user_input in choices:
        return user_input

    # User inputted a hidden choice
    elif user_input in hidden_choices:
        if user_input == "list":
            display_choices(choices)
            return choice_from_list(choices, hidden_choices)
        return user_input

    # User may have used an abbreviation
    else:
        abbreviation_choices = {}
        for choice in choices:
            # if a choice has
            # abbreviations, add them to abbreviation_choices
            if choice in abbreviations.keys():
                abbreviation_choices[choice] = abbreviations.get(choice)
        abbreviation_choices_hidden = {}
        for choice in hidden_choices:
            # if a hidden_choice has
            # abbreviations, add them to abbreviation_choices_hidden
            if choice in abbreviations.keys():
                abbreviation_choices_hidden[choice] = \
                    abbreviations.get(choice)

        possible_choices = get_keys_from_value(user_input,
                                               abbreviation_choices)
        possible_choices_hidden = \
            get_keys_from_value(user_input,
                                abbreviation_choices_hidden)

        # If multiple choices with matching abbreviations were found
        if len(possible_choices + possible_choices_hidden) > 1:
            # If already a layer deep in recursion, do not add ""
            print("There are multiple choices with that abbreviation. "
                  "Pick one: ", possible_choices)
            mult_choice = choice_from_list(possible_choices,
                                           possible_choices_hidden + [""]
                                           if [""] not in
                                              possible_choices_hidden
                                           else possible_choices_hidden)
            # User wants to go back
            if mult_choice == "":
                return choice_from_list(choices, hidden_choices)

            # User wants a list of choices
            elif mult_choice == "list":
                display_choices(choices)
                return choice_from_list(choices, hidden_choices)

            # User picked a valid choice from the multiple matching choices
            return mult_choice

        # No abbreviations matched the user's input
        elif len(possible_choices + possible_choices_hidden) < 1:
            print("No matching choices")
            # TODO: Allow user to add abbreviation here
            return choice_from_list(choices, hidden_choices)

        # Only one possible choice the abbreviation referred to
        else:

            # User chose a visible choice's abbreviation
            if len(possible_choices) > 0:
                return possible_choices[0]

            # User chose a list abbreviation
            if possible_choices_hidden[0] == "list":
                display_choices(choices)
                return choice_from_list(choices, hidden_choices)

            # User chose a hidden choice's abbreviation
            return possible_choices_hidden[0]
