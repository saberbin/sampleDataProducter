# sampleKafkaProducter
简单的Kafka测试数据生成项目，是另一个项目的测试数据生成项目。
> https://github.com/saberbin/Kafka2FileSystem.git

目的是为了持续不断的生成测试用的字符串数据发送到Kafka。
可以输出按分隔符分割的字符串数据以及json字符串，输出方式可以是Kafka、文件（txt文件）、终端。
## 环境配置
python版本建议大于3.6
```shell
conda create -n skproducter python=3.8.10
# 安装以下第三方库
pip install kafka-python
pip install fake
# 或者是安装requirements文件：pip install -r ./requirements.txt
```

## run project 启动项目
项目主程序（main program）：sampleKafkaProducter.py
```shell
git clone https://github.com/saberbin/sampleKafkaProducter.git
cd sampleKafkaProducter
# 携带参数执行
python ./sampleKafkaProducter.py --config ./settings/defaultConf_text.conf
python ./sampleKafkaProducter.py --datatype json --num 10 --output file --outputfile ./data/
python ./sampleKafkaProducter.py --datatype text --patter , --num 10 --output file --outputfile ./data/
python ./sampleKafkaProducter.py --datatype text --patter , --num 10 --output shell
# output data in terminal
>>>1;李岩;107;F;lichang@yahoo.com;1916-02-25;2024-01-13
>>>2;王秀云;13;F;lei34@yahoo.com;2010-05-18;2024-01-13
>>>3;王秀云;59;F;lihuang@gmail.com;1964-12-26;2024-01-13
>>>4;陈秀荣;81;F;izhou@gmail.com;1943-01-27;2024-01-13
>>>5;张桂兰;55;M;qiang28@gmail.com;1968-10-31;2024-01-13

# 如果不携带参数，则会在终端输出100行数据
python ./sampleKafkaProducter.py
```

## 项目启动参数
项目传参方式有两种：配置文件、启动传参。
优先级上，配置文件的优先级是最高的，只有在不传入`--config`的情况下才会解析其他的传参。如果传入的配置文件路径不存在，则会直接抛出`FileNotFoundError`的异常，程序会直接终止。
### 配置文件传参
配置文件传参也是需要启动的时候传入`--config`进行配置，如：
```shell
python ./sampleKafkaProducter.py --config ./settings/defaultConf_text.conf
```
配置文件可以按照以下配置进行设置，根据输出类型以及输出方式的不同可能会有点不同。
```text
# 使用#进行注释，#后面的内容都不会进行解析
datatype=text  # json或者text，text类型为按某分隔符分隔的字符串行数据
datapatter=;  # json类不需要此配置，text类则配置为对应的分隔符，不建议使用#作为分隔符，可能会导致程序出错
num=10
output=kafka  # 输出方式，可选值：kafka、file、shell
outputfile=/home/saberbin/project/sampleKafkaProducter/data  # 输出方式为file的时候才会读取该配置
# kafka相关配置，输出方式为kafka的时候才会读取
bootstrapservers=172.26.254.80:9092  # kafkaIP地址端口，多个地址使用“,”分隔
topic=test  # Kafka的topic名称
```
可以根据具体的需求选择。
需要注意的是，如果配置文件中缺少配置参数，启动传参也传入了该参数，则程序不会读取启动参数值，只会以配置文件的为主，然后如果该参数是必要参数可能会导致程序异常停止。
### 启动传参
具体参数与配置文件的参数是一致的。
```shell
python ./sampleKafkaProducter.py --datatype json --num 10 --output shell

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
目前配置中没有设置切换模型类的参数配置，如果需要切换则需要在`sampleKafkaProducter.py`中的`from module.user import UserGenerator`切换为自定义的模型数据生成类。


# TODO
- 输出到socket端口
- 添加数据类切换配置参数
- 简易数据类生成方法及配置

