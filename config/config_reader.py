import configparser


def read_config_data(section, key):
    file = 'config/config.ini'
    config = configparser.ConfigParser()
    config.read(file)
    return config[section][key]
