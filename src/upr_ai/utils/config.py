import yaml

from upr_ai.utils.Exception import FileError, UnknownError


class ConfigManager:
    """Loads the configuration"""

    def __init__(self, config_path: str) -> None:
        """Load config_path and config

        Args:
            config_path (str): file path to the configuration to load

        Get configuration using:
            get_config: attribute to get the loaded configuration

        """
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self) -> dict:
        """function to load the configuration

        Returns:
            configuration (dict)
        """

        try:
            with open(self.config_path, encoding="utf-8") as file:
                return yaml.safe_load(file)

        except TypeError as exc:
            raise FileError("File Error", original_exception=exc) from exc

        except FileNotFoundError as exc:
            raise FileError("File Error", original_exception=exc) from exc

        except yaml.YAMLError as e:
            raise FileError("File Error", original_exception=e) from e

        except Exception as exc:
            raise UnknownError("Unknown Error", original_exception=exc) from exc

    def get_config(self) -> dict:
        """_summary_

        Returns:
            configuration (dict)
        """
        return self.config
