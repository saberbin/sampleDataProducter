from dataclasses import dataclass
from json import dumps


@dataclass
class User(object):
    id: int
    name: str
    age: int
    sex: str
    mail: str
    create_time: str
    update_time: str

    def to_str(self, data_type='text', patter="|") -> str:
        if data_type == "text":
            attr_list = [str(item) for item in list(self.__dict__.values())]
            return f"{patter}".join(attr_list)
        elif data_type.lower() == "json":
            return dumps(self.__dict__, ensure_ascii=False)
        else:
            return None


@dataclass
class Word(object):
    word: str
    
    def to_str(self, data_type='text') -> str:
        if data_type == "text":
            return self.word
        elif data_type.lower() == "json":
            
            return dumps({"word": self.word}, ensure_ascii=False)
        else:
            return None


@dataclass
class UserClickInfo(object):
    timestamp: str
    area: str
    city_name: str
    user_id: int
    ad_id: int
    
    def to_str(self, data_type='text', patter="|") -> str:
        if data_type.lower() == "text":
            attr_list = [str(item) for item in list(self.__dict__.values())]
            return f"{patter}".join(attr_list)
        elif data_type.lower() == "json":
            return dumps(self.__dict__, ensure_ascii=False)
        else:
            return None



