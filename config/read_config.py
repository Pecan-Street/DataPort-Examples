import configparser
import traceback


def get_database_config(config_file):
    try:
        config = configparser.ConfigParser()
        config.read(config_file)
        return {
            "hostname": config.get("database_config", "hostname"),
            "username": config.get("database_config", "username"),
            "password": config.get("database_config", "password"),
            "port": int(config.get("database_config", "port")),
            "database": config.get("database_config", "database")
        }
    except configparser.Error as e:
        traceback.print_exc()
        print(
            "Error reading database configuration. Does the config/config.txt file exist and have entries for "
            "hostname, username, password, database, and port?")
        exit(1)
