import configparser
import os

config = configparser.ConfigParser()
if os.path.exists("data"):
    file_path = 'config.ini'
else:
    file_path = 'chess/config.ini'

config.read(file_path)
AUTOMATIC_FILL = config.getboolean('Settings', 'automatic_fill')
EXPORT_TO_FILE = config.getboolean('Settings', 'export_to_file')
FAVORITE_COLOR = config.get('Settings', 'favorite_color')
PLAYER_LIST_ORDER = config.get('Settings', 'player_list_order')
