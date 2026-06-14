from upr_ai.utils.config import ConfigManger


def test_config():
    """test config module if it functions properly"""
    file_path = "config/logging_config.yaml"
    config_manager = ConfigManger(file_path)
    config = config_manager.get_config()
    assert type(config) == type({})
    assert len(config) != 0
    assert config != None
