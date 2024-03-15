# sampleDataProducter
简单的测试数据生成项目，是另一个项目的测试数据生成项目。
> https://github.com/saberbin/Kafka2FileSystem.git

目的是为了持续不断的生成测试用的字符串数据发送到Kafka。
可以输出按分隔符分割的字符串数据以及json字符串，输出方式可以是Kafka、文件（txt文件）、终端。
## 环境配置
python版本建议大于3.6
```shell
conda create -n sdproducter python=3.8.10
# 安装以下第三方库
pip install kafka-python
pip install fake
# 或者是安装requirements文件：pip install -r ./requirements.txt
```

## run project 启动项目
项目主程序（main program）：sampleDataProducter.py
```shell
git clone https://github.com/saberbin/sampleDataProducter.git
cd sampleDataProducter
# 携带参数执行
python ./sampleDataProducter.py --config ./settings/defaultConf_text.conf
python ./sampleDataProducter.py --datatype json --num 10 --output file --outputfile ./data/
python ./sampleDataProducter.py --datatype text --patter , --num 10 --output file --outputfile ./data/
python ./sampleDataProducter.py --datatype text --patter , --num 10 --output shell
# output data in terminal
>>>1;李岩;107;F;lichang@yahoo.com;1916-02-25;2024-01-13
>>>2;王秀云;13;F;lei34@yahoo.com;2010-05-18;2024-01-13
>>>3;王秀云;59;F;lihuang@gmail.com;1964-12-26;2024-01-13
>>>4;陈秀荣;81;F;izhou@gmail.com;1943-01-27;2024-01-13
>>>5;张桂兰;55;M;qiang28@gmail.com;1968-10-31;2024-01-13

# 如果不携带参数，则会在终端输出100行数据
python ./sampleDataProducter.py
```

## 项目启动参数
项目传参方式有两种：配置文件、启动传参。
优先级上，配置文件的优先级是最高的，只有在不传入`--config`的情况下才会解析其他的传参。如果传入的配置文件路径不存在，则会直接抛出`FileNotFoundError`的异常，程序会直接终止。
### 配置文件传参
配置文件传参也是需要启动的时候传入`--config`进行配置，如：
```shell
python ./sampleDataProducter.py --config ./settings/defaultConf_text.conf
```
配置文件可以按照以下配置进行设置，根据输出类型以及输出方式的不同可能会有点不同。
```text
# 使用#进行注释，#后面的内容都不会进行解析
datatype=text  # json或者text，text类型为按某分隔符分隔的字符串行数据
datapatter=,  # json类不需要此配置，text类则配置为对应的分隔符，不建议使用#作为分隔符，可能会导致程序出错
num=10
output=shell  # 输出方式，可选值：kafka、file、shell
outputfile=/home/saberbin/project/sampleDataProducter/data  # 输出方式为file的时候才会读取该配置
# kafka相关配置，输出方式为kafka的时候才会读取
bootstrapservers=172.21.40.103:9092  # kafkaIP地址端口，多个地址使用“,”分隔
topic=test  # Kafka的topic名称
datagenerator=UserClickGenerator  # 数据生成类模块名称，自定义的情况建议与数据类模块放一个文件以免无法加载导致报错
datagenmodule=null  # 数据生成类模块文件的存放路径
delay=5  # 输出延时，默认为0.1秒，控制输出到Kafka以及终端的速率
```
可以根据具体的需求选择。
需要注意的是，如果配置文件中缺少配置参数，启动传参也传入了该参数，则程序不会读取启动参数值，只会以配置文件的为主，然后如果该参数是必要参数可能会导致程序异常停止。
### 启动传参
具体参数与配置文件的参数是一致的。
```shell
python ./sampleDataProducter.py --datatype json --num 10 --output shell

>>>{"id": 1, "name": "李淑兰", "age": 15, "sex": "M", "mail": "pli@yahoo.com", "create_time": "2008-10-19", "update_time": "2024-01-14"}
>>>{"id": 2, "name": "张瑞", "age": 20, "sex": "M", "mail": "fangshi@hotmail.com", "create_time": "2003-03-19", "update_time": "2024-01-14"}
>>>{"id": 3, "name": "张丹丹", "age": 59, "sex": "M", "mail": "yongyin@yahoo.com", "create_time": "1964-05-27", "update_time": "2024-01-14"}
>>>{"id": 4, "name": "周彬", "age": 34, "sex": "M", "mail": "tding@hotmail.com", "create_time": "1989-11-06", "update_time": "2024-01-14"}
>>>{"id": 5, "name": "李欣", "age": 72, "sex": "M", "mail": "zhangqiang@yahoo.com", "create_time": "1951-08-24", "update_time": "2024-01-14"}
>>>{"id": 6, "name": "朱洁", "age": 15, "sex": "F", "mail": "ganglong@hotmail.com", "create_time": "2008-09-26", "update_time": "2024-01-14"}
>>>{"id": 7, "name": "王鑫", "age": 6, "sex": "F", "mail": "xiabai@gmail.com", "create_time": "2017-08-22", "update_time": "2024-01-14"}
>>>{"id": 8, "name": "郭慧", "age": 41, "sex": "M", "mail": "junhuang@hotmail.com", "create_time": "1983-01-18", "update_time": "2024-01-14"}
>>>{"id": 9, "name": "张丽华", "age": 110, "sex": "M", "mail": "jie01@yahoo.com", "create_time": "1913-09-19", "update_time": "2024-01-14"}
>>>{"id": 10, "name": "周欢", "age": 103, "sex": "M", "mail": "liangxiuying@yahoo.com", "create_time": "1920-10-17", "update_time": "2024-01-14"}
```
传参都设置了默认值，如果直接启动程序是可以在终端输出的。

## 数据模型
此处为旧版的内容：
输出的数据是以项目目录下的`module.user`中的`User`数据模型生成数据的，`UserGenerator`类则负责创建`User`对象及输出。如下：
```python
from dataclasses import dataclass
from faker import Faker
from datetime import datetime, date, timedelta
from random import randint
import json


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
            return json.dumps(self.__dict__, ensure_ascii=False)
        else:
            return None


class UserGenerator(object):
    def __init__(self) -> None:
        self.fake = Faker(locale="zh_CN")

    def make_user(self, user_id=None, data_type='text', patter="|") -> User:
        if user_id is None:
            user_id = randint(1, 999)
        user_info = self.fake.simple_profile(sex=None)
        user = User(
            id=user_id,
            name=user_info.get("name"),
            age=self.cal_age(user_info.get("birthdate")),
            sex=user_info.get("sex"),
            mail=user_info.get("mail"),
            create_time=str(user_info.get("birthdate")),
            update_time=str(date.today())
        )
        return user.to_str(data_type=data_type, patter=patter)

    @staticmethod
    def cal_age(birthday: date) -> int:
        """
        计算出生日期与今天的日期的天数差的年数
        两个日期之间相减得到相差的天数，按照365计算求年数
        """
        result = date.today() - birthday
        return result.days // 365

```
如果想要实现输出自定义的数据，可以按照上述模型自定义自己的数据类，需要注意的是需要实现`to_str`的方法，输出字符串的数据，因为输出方式为`Kafka`的时候默认了`str`类型。数据对象的生成类也需要实现。
目前配置中没有设置切换模型类的参数配置，如果需要切换则需要在`sampleDataProducter.py`中的`from module.user import UserGenerator`切换为自定义的模型数据生成类。

此处为重构之后的内容(2024-03)：
之前数据类是单独的模块存放，重构后都放置到`module.DataModule`模块文件中，定义的方式没有改变。数据生成器类也都汇总到了`module.dataGenerator`模块中，所有具体的数据生成类都应该继承自抽象类`DataGenerator`并实现对应的抽象方法。
```python
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

```
### 数据模型的加载
为了可以自定义传入的数据生成类以及数据类，修改了项目启动传参等，添加了自定义数据的传参参数。
实际的代码层面，是通过`importlib`模块去动态加载数据生成类，默认情况下搜索当前项目目录下的`module`目录的模块。
所以在自定义的时候需要传入模块名称以及模块对应的目录，最好是绝对路径。
主程序中通过方法去构建数据生成类的模块的路径以及加载对应的数据生成类
```python

    def __load_dataGen_module_path(self, datagenmodule: str) -> str:
        """
        构建数据生成器模块的加载路径
        """
        if (datagenmodule=="null") or (datagenmodule is None):
            module_dir = self.workpath.joinpath(Constant.datagenerator_class_module_dir)
            datagenmodule = module_dir.joinpath(Constant.datagenerator_class_module_file)
            # 重新设置回常量配置类中，然后下面从这个配置类中取出该路径动态加载
            Constant.update_attr("datagenerator_module_path", str(datagenmodule))
        else:
            # 传入的参数应该是绝对路径，根据这个绝对路径加载数据生成类
            Constant.update_attr("datagenerator_module_path", datagenmodule)
        
        dataGenModulePath = Constant.datagenerator_module_path
        if dataGenModulePath is None:
            raise ValueError("dataGenModulePath设置失败，无法加载数据生成类，请检查代码。")
        
        return dataGenModulePath

    def make_data_generator(self, datagenerator: str, dataGenModulePath: str) -> DataGenerator:
        """
        根据数据生成器模块路径，利用importlib动态加载，返回对应的数据生成器类
        """
        # 从常量配置中获取数据生成类的模块路径
        spec = importlib.util.spec_from_file_location(datagenerator, dataGenModulePath)
        data_module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = data_module
        spec.loader.exec_module(data_module)
        gen_class = getattr(data_module, datagenerator)
        return gen_class()  # 返回实例化的对象
```
`gen_class()`是数据生成类的实例化方法，最后返回的数据生成类的实例化对象。
其中加载过程的默认参数放在了`common.constant`模块中
```python
    # 数据生成器类的模块名称以及模块文件名
    datagenerator_class_module_dir: str = "module"
    datagenerator_class_module: str = "dataGenerator"
    datagenerator_class_module_file: str = "dataGenerator.py"
    datagenerator_module_path: str = None
```


# TODO
- 输出到socket端口
- 简易数据类生成方法及配置

