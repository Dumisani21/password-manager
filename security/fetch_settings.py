import json, os

def fetch_pass():
    path_location = os.path.join(os.path.expanduser('~'), '.eagle_eye/config.json')
    if os.path.exists(path_location):
        with open(path_location, 'r') as fp:
            password = json.load(fp)
    return password['master_password']

def fetch_db_location():
    path_location = os.path.join(os.path.expanduser('~'), '.eagle_eye/config.json')
    if os.path.exists(path_location):
        with open(path_location, 'r') as fp:
            db = json.load(fp)
    return db['db_location']


def check_main_dir():
    path_location = os.path.join(os.path.expanduser('~'), '.eagle_eye')
    if os.path.exists(path_location):
        path_location = path_location = os.path.join(os.path.expanduser('~'), '.eagle_eye/config.json')
        path_db_location = path_location = os.path.join(os.path.expanduser('~'), '.eagle_eye/database')
        if os.path.exists(path_location) and os.path.exists(path_db_location):
            path_db_file = path_location = os.path.join(os.path.expanduser('~'), '.eagle_eye/database/psw_manager.db')
            if os.path.exists(path_db_file):
                return True
    return False