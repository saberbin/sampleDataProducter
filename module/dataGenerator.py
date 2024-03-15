from abc import ABC, abstractmethod
from typing import Any, Dict, List, Union
from faker import Faker
from datetime import datetime, date, timedelta
from random import randint
from random import randint, choices
from string import ascii_letters, digits
from module.DataModule import *



class DataGenerator(ABC):
    _instance = None
    DATATYPE: str = "data_type"
    INDEX: int = "index"
    PATTER: str = "patter"
    PARAMS: List[str] = []

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    @classmethod
    def __get_class_params(cls) -> List[str]:
        return list(cls.__annotations__.keys())

    @classmethod
    def method_param(cls, param_name: str) -> Any:
        params = cls.__get_class_params()
        if param_name in params:
            return cls.__getattribute__(param_name)
        else:
            raise ValueError(f"传入的{param_name}参数名错误")

    def necessary_params(self):
        return self.PARAMS

    @abstractmethod
    def param_check(self):
        """
        True: 表示当前参数需要传入
        False: 表示当前参数不需要传入
        None: 表示当前数据生成器类的make_data方法不需要传入参数
        """
        ...

    @abstractmethod
    def make_data(self):
        """数据生成器的数据生成方法"""
        ...
        
    @abstractmethod
    def get_data_class_name(self):
        ...


class WordGenerator(DataGenerator):
    PARAMS = ["data_type"]
    def __init__(self) -> None:
        self.words = ascii_letters + digits

    def necessary_params(self):
        return self.PARAMS

    def param_check(self, *args) -> Union[bool, None]:
        """当前数据生成器方法不需要传入参数"""
        return None

    def make_data(self, data_type: str="text", *args, **kwargs) -> Any:
        local_params = {"data_type": data_type}
        if kwargs:
            for key, value in kwargs.items():
                if self.param_check(key):
                    local_params[key] = value
        k: int = randint(3, 10)
        word = Word("".join(choices(self.words, k=k)))
        return word.to_str(data_type=local_params.get("data_type"))

    def get_data_class_name(self):
        return "Word"


class UserGenerator(DataGenerator):
    PARAMS = ["user_id", "data_type", "patter"]
    def __init__(self) -> None:
        self.fake = Faker(locale="zh_CN")

    def necessary_params(self) -> List[str]:
        """
        获取当前生成器的数据生成方法的参数列表
        """
        return self.PARAMS

    def param_check(self, param_name: str) -> Union[bool, None]:
        return self.PARAMS.__contains__(param_name)

    @staticmethod
    def __get_user_id() -> int:
        return randint(1, 999)
    
    def make_data(self, data_type, *args, id=None, patter=None, **kwargs) -> User:
        local_params = {
            "user_id": None, "data_type": data_type, "patter": None
        }
        if kwargs:
            for key, value in kwargs.items():
                if self.param_check(key):
                    local_params[key] = value
                if key == "id":
                    local_params['user_id'] = id
        else:
            if id is None:
                user_id = self.__get_user_id()
                local_params['user_id'] = user_id
            else:
                local_params['user_id'] = id
            if patter is None:
                local_params['patter'] = "|"
            else:
                local_params['patter'] = patter
        user_info = self.fake.simple_profile(sex=None)
        user = User(
            id=local_params.get("user_id"),
            name=user_info.get("name"),
            age=self.cal_age(user_info.get("birthdate")),
            sex=user_info.get("sex"),
            mail=user_info.get("mail"),
            create_time=str(user_info.get("birthdate")),
            update_time=str(date.today())
        )
        return user.to_str(data_type=local_params.get("data_type"), patter=local_params.get("patter"))
    
    @staticmethod
    def cal_age(birthday: date) -> int:
        """
        计算出生日期与今天的日期的天数差的年数
        两个日期之间相减得到相差的天数，按照365计算求年数
        """
        result = date.today() - birthday
        return result.days // 365

    def get_data_class_name(self):
        return "User"


class UserClickGenerator(DataGenerator):
    PARAMS = ["data_type"]
    def __init__(self) -> None:
        cityinfo = """1	北京	华北
2	上海	华东
3	深圳	华南
4	广州	华南
5	武汉	华中
6	南京	华东
7	天津	华北
8	成都	西南
9	哈尔滨	东北
10	大连	东北
11	沈阳	东北
12	西安	西北
13	长沙	华中
14	重庆	西南
15	济南	华东
16	石家庄	华北
17	银川	西北
18	杭州	华东
19	保定	华北
20	福州	华南
21	贵阳	西南
22	青岛	华东
23	苏州	华东
24	郑州	华北
25	无锡	华东
26	厦门	华南"""
        self.city_data = []
        for line in cityinfo.splitlines():
            values = line.strip().split("\t")
            self.city_data.append((values[0], values[1], values[2]))
        self.city_nums = len(self.city_data)

    @staticmethod
    def get_current_time() -> str:
        return str(datetime.now())

    def necessary_params(self) -> List[str]:
        """
        获取当前生成器的数据生成方法的参数列表
        """
        return self.PARAMS

    def param_check(self, param_name: str) -> Union[bool, None]:
        return self.PARAMS.__contains__(param_name)

    @staticmethod
    def get_randint(num1: int, num2: int) -> int:
        return randint(num1, num2)

    @staticmethod
    def get_id() -> int:
        return randint(1, 6)

    def get_city(self, index: int) -> str:
        city_info = self.city_data[index]
        return city_info[1]

    def get_area(self, index: int) -> str:
        city_info = self.city_data[index]
        return city_info[2]

    def make_data(self, data_type: str="text", *args, **kwargs) -> Any:
        local_params = {"data_type": data_type, "id": None, "ad_id": None, "patter": ","}
        if kwargs:
            for key, value in kwargs.items():
                if self.param_check(key):
                    local_params[key] = value
        if data_type is None:
            local_params['data_type'] = "text"
        if local_params.get("id", None) is None:
            local_params['id'] = self.get_id()
        if local_params.get("ad_id", None) is None:
            local_params['ad_id'] = self.get_id()
        city_index = randint(0, self.city_nums-1)
        
        user_click = UserClickInfo(
            timestamp=self.get_current_time(),
            area=self.get_area(city_index),
            city_name=self.get_city(city_index),
            user_id=local_params.get("id"),
            ad_id=local_params.get("ad_id")
        )
        return user_click.to_str(data_type=local_params.get("data_type"), patter=local_params.get("patter"))

    def get_data_class_name(self):
        return "UserClickInfo"