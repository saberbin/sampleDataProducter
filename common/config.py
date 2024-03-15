from pathlib import Path
from typing import Any, Union


class Config(object):
    """
    项目配置信息类
    项目启动参数以及项目配置文件信息参数都由此类给出，
    即最终程序执行的参数都会汇总在此类。
    """
    
    ValueType = {
        "datatype": str,
        "datapatter": str,
        "num": int,
        "output": str,
        "outputfile": str,
        "bootstrapservers": str,
        "topic": str,
        "datagenerator": str,
        "datagenmodule": str,
        "delay": float
    }
    
    def __init__(self, config_path: Union[Path, None]) -> None:
        self.config_path = None if config_path is None else self.__load_config_path(config_path)
        self.config_items = dict()  # 初始化字典存放配置参数
    
    @staticmethod
    def __load_config_path(config_path: Path) -> Path:
        if isinstance(config_path, Path):
            return config_path
        else:
            return Path(config_path)

    def read_data(self) -> None:
        """
        配置文件读取方法，如果配置文件为空则直接返回空；
        如果配置文件不存在则会直接抛出FileNotFoundError的异常；
        否则会按行读取文件，按照等号(=)对参数以及参数值进行分割，最终将参数设置到对象config_items属性中
        """
        if self.config_path is None:
            return None  # 配置文件不存在直接返回
        if not self.config_path.exists():
            raise FileNotFoundError(f"{self.config_path}配置文件不存在。")
        with open(self.config_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for line in lines:
            if not line:
                # 跳过空行
                continue
            if line.startswith("#"):
                continue
            elif "#" in line:
                line, *_ = line.split("#")
            attr_name, attr_value = line.strip().split("=")
            self.set_config(key=attr_name, value=attr_value)

    def set_config(self, key: str, value: Any) -> None:
        """设置配置参数到config_items属性中"""
        type_check_result = self.__value_type_check(key, value)
        if type_check_result is None:
            return 
        elif type_check_result:
            self.config_items[key] = value
        else:
            self.config_items[key] = self.__value_type_change(key, value)
    
    def get_value(self, key):
        """获取参数值
        从对象config_items属性中获取参数值，如果该参数不存在则会返回空，否则返回参数值
        """
        return self.config_items.get(key, None)

    def is_empty(self) -> bool:
        """判断配置参数是否为空"""
        if len(self.config_items) == 0:
            return True
        return False

    @classmethod
    def __value_type_check(cls, key: str, value:Any) -> Any:
        """检查配置参数数据类型是否符合目标数据类型"""
        value_type = cls.ValueType.get(key)
        if value_type is None:
            return None  # 传入不期望的参数不做处理
        elif isinstance(value, value_type):
            return True
        else:
            return False

    @classmethod
    def __value_type_change(cls, key, value: Any) -> Any:
        """将不符合的参数数据类型转换为目标数据类型"""
        type_func = cls.ValueType[key]
        return type_func(value)

