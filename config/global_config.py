# config/global_config.py

import yaml


class GlobalConfig:
    _config = None

    @classmethod
    def load_config(cls, file_path):
        with open(file_path, 'r') as file:
            cls._config = yaml.safe_load(file)

    @classmethod
    def get_config(cls):
        if cls._config is None:
            raise ValueError("Configuration not loaded. Call 'load_config' first.")
        return cls._config


# 初始化配置
config_file_path = 'config/config.yml'
GlobalConfig.load_config(config_file_path)
