from typing import Dict

import yaml


# 读取 YAML 配置文件的函数
def read_config(file_path: str) -> Dict:
    """读取 YAML 配置文件并返回数据"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            config_data = yaml.safe_load(f)
            return config_data
    except FileNotFoundError:
        raise f"配置文件 {file_path} 未找到"
    except yaml.YAMLError as e:
        raise f"读取配置文件时出错: {e}"


def initConfig(path: str) -> Dict:
    return read_config(path)
