import sys

import yaml
from typing import Dict

from upr_ai.utils.Exception import CustomException


class ConfigManger:
    """Loads the configuration"""

    def __init__(self, config_path: str):
        """Load config_path and config

        Args:
            config_path (str): file path to the configuration to load

        Get configuration using:
            get_config: attribute to get the loaded configuration

        """
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self) -> Dict:
        """function to load the configuration

        Returns:
            configuration (dict)
        """

        try:
            with open(self.config_path, "r", encoding="utf-8") as file:
                return yaml.safe_load(file)
        except TypeError:
            raise TypeError("Config Path should be a string")
        except FileNotFoundError:
            raise FileNotFoundError(f"NO file named {self.config_path} was found")

    def get_config(self) -> Dict:
        """_summary_

        Returns:
            configuration (dict)
        """
        return self.config
