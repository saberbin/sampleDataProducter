from abc import ABC, abstractmethod
from typing import Any, Union, List, Dict
from pathlib import Path
from time import sleep
from common.utils import generate_random_str
from common.kafka_producer import kafkaProducer


class Output(object):
    """抽象类，定义输出的基本方法"""
    outputType = ['kafka', 'file', 'shell']
    
    def __init__(self, output_type="shell") -> None:
        self.output_type = self.__check_output_type(output_type)
        self.output_obj = None

    def __check_output_type(self, type_name: str) -> str:
        if type_name.lower() in Output.outputType:
            return type_name.lower()

    @abstractmethod
    def __conn_output(self, *args, **kwargs) -> Any:
        ...

    @abstractmethod
    def output_data(self, message, **kwargs) -> None:
        ...


class KafkaOutput(Output):
    def __init__(self, bootstrapservers, topic, output_type="kafka", *args, **kwargs) -> None:
        super().__init__(output_type)
        self.output_obj: kafkaProducer = self.__conn_output(bootstrapservers, topic, *args, **kwargs)
    
    def __conn_output(self, bootstrapservers, topic) -> kafkaProducer:
        kp = kafkaProducer(bootstrap_servers=bootstrapservers)
        kp.set_topic(topic=topic)
        return kp

    def output_data(self, message: str, **kwargs) -> None:
        if kwargs:
            if "delay" in kwargs.keys():
                self.output_obj.send_msg(message, delay=kwargs.get("delay"))
        else:
            self.output_obj.send_msg(message)


class FileOutput(Output):
    def __init__(self, file_path, output_type="file", *args, **kwargs) -> None:
        super().__init__(output_type)
        self.output_obj = self.__conn_output(file_path, *args, **kwargs)

    @staticmethod
    def __check_extsis(file_path: Path) -> bool:
        if file_path.exists():
            return True
        else:
            return False
    
    @staticmethod
    def __is_file(file_path: Path) -> bool:
        return file_path.is_file()

    @staticmethod
    def __create_file(file_path: Path) -> None:
        file_path.mkdir(mode=777, parents=True)

    def __conn_output(self, file_path: Union[str, Path], *args, **kwargs) -> Any:
        if isinstance(file_path, Path):
            return file_path
        return Path(file_path)

    def __check_path(self):
        if self.__is_file(self.output_obj):
            # 对象为文件
            # 判断文件的父级目录是否存在
            # parent_path = Path(self.output_obj.parent_path)
            if self.__check_extsis(self.output_obj.parent):
                pass
            else:
                # 父级目录不存在则创建
                self.__create_file(self.output_obj.parent)
        else:
            # 对象非文件，即为目录，则创建一个随机文件名称的文件作为存放目录
            self.output_obj = self.output_obj.joinpath(generate_random_str() + ".txt")

    def output_data(self, message: str, **kwargs) -> None:
        self.__check_path()  # 检测目录及处理
        # 追加的形式写入文件
        with open(self.output_obj, "a+", encoding="utf-8") as f:
            f.write(message)
            f.write("\n")


class SysOutput(Output):
    def __init__(self, output_type="shell", *args, **kwargs) -> None:
        super().__init__(output_type)
        self.output_obj: None = self.__conn_output(*args, **kwargs)

    def __conn_output(self, *args, **kwargs) -> Any:
        return None

    def output_data(self, message: Any, **kwargs) -> None:
        if kwargs.get("delay"):
            sleep(kwargs.get("delay"))
        print(f">>>{message}")


class OutputFactory(object):
    def __init__(self) -> None:
        self.outputObj = None

    def make_output(self, output_type: str, *args, **kwargs) -> None:
        if output_type == "kafka":
            bootstrapservers = kwargs.get("bootstrapservers")
            topic = kwargs.get("topic")
            self.outputObj = KafkaOutput(bootstrapservers=bootstrapservers, topic=topic)
        elif output_type == "file":
            output_file = kwargs.get("output_path")
            self.outputObj = FileOutput(file_path=output_file)
        elif output_type == "shell":
            self.outputObj = SysOutput()
        else:
            raise ValueError(f"output object not support for {output_type} type")

    def get_output_obj(self) -> Output:
        return self.outputObj

