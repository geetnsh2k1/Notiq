import os
from configparser import ConfigParser
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # Load APP_ENV from .env file

class ConfigClient:
    _config = None

    @classmethod
    def load_config(cls):
        env = os.getenv("APP_ENV", "local").lower()
        base_path = Path(__file__).parent

        base_config_file = base_path / "base.ini"
        env_config_file = base_path / env / "application.ini"

        config = ConfigParser()
        config.read(base_config_file)
        config.read(env_config_file)

        cls._config = config

    @classmethod
    def get_property(cls, key: str, section: str = "DEFAULT", default=None):
        if cls._config is None:
            cls.load_config()
        return cls._config[section].get(key, default)
