from pathlib import Path
from common.utils import get_workpath
from typing import Any


class Constant(object):
    workpath: Path = get_workpath()
    data_path: str = "data"
    settings_path: str = "settings"
    setting_file: str = "defaultConf_text.conf"
    # 数据生成器类的模块名称以及模块文件名
    datagenerator_class_module_dir: str = "module"
    datagenerator_class_module: str = "dataGenerator"
    datagenerator_class_module_file: str = "dataGenerator.py"
    datagenerator_module_path: str = None

    @classmethod
    def update_attr(cls, attr_name: str, attr_value: Any) -> None:
        """如果类属性存在则设置，否则抛出属性不存在的异常"""
        if hasattr(cls, attr_name):
            setattr(cls, attr_name, attr_value)
        else:
            raise AttributeError()

