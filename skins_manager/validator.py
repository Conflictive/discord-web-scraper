"""
skins_manager.validator
~~~~~~~~~~~~~~~~~~~~~~~
This module is used to check if the users input is a legitimate skin.

Dependencies:
    - storage: Module to get the legitimate list of skins
"""

import skins_manager.storage as storage


def check_skin(user_input):
    """
    Compares user input to the list of valid skins

    Returns:
        - True: if the skin exists
        - False: if it does not exist
    """
    skins = storage.open_skin_file()

    if user_input in skins:
        return True

    return False
