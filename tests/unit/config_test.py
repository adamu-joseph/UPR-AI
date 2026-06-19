from upr_ai.utils.config import ConfigManager


def test_config():
    """test config module if it functions properly"""
    file_path = "config/logging_config.yaml"
    config_manager = ConfigManager(file_path)
    config_manager.get_config()
