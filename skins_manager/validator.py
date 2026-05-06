import skins_manager.storage as storage


def check_skin(user_input):
    """Compares user input to the list of valid skins"""
    skins = storage.open_skin_file()

    if user_input in skins:
        return True

    return False
