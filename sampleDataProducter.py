import sys
from typing import Any, Union, List
from common.argsParser import ArgsParser
from common.config import Config
from module.DataModule import *  # 所有的数据类都写在这个文件中
from module.dataGenerator import *  # 对应的数据类的数据生成类写在这个文件中
from common.output import OutputFactory
from common.constant import Constant
import importlib


class sampleDataProducter(object):
    def __init__(self, name: str, args: Any) -> None:
        self.workpath = Constant.workpath  # 获取项目工作目录
        self.config = self.__parser_all_config(name=name, args=args)  # 解析配置参数
        self.outputObj = None  # 初始化输出对象为空

    def __parser_all_config(self, name: str, args: List[Any]):
        # 解析项目启动传参
        args_parser = ArgsParser(name)
        args_parser.parse_args(args=args)
        
        # 解析配置文件
        config_path = args_parser.get_value("config")
        config = Config(config_path=config_path)
        config.read_data()
        
        # 如果配置文件路径不存在，配置参数为空，
        # 那么则从启动传参中获取配置参数
        # 如果用户启动的时候也没有传参，则会获取默认的参数配置
        if config.is_empty():
            for key, value in args_parser.arg_items.items():
                config.set_config(key=key, value=value)
        return config

    def __get_config_value(self, key: str) -> Any:
        """获取配置文件的参数"""
        return self.config.get_value(key)

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

    @staticmethod
    def __gen_data(data_type: str, dataGen:DataGenerator, *args, **kwargs) -> Any:
        return dataGen.make_data(data_type, *args, **kwargs)

    def gen_data(self, dataGen: DataGenerator, data_type: str, nums: int=100, patter="|") -> str:
        """数据生成器"""
        for index in range(nums):
            yield self.__gen_data(data_type, dataGen, id=index, patter=patter)

    def __make_outputObj(self) -> None:
        """构造输出对象实例，用于输出数据"""
        output_factory = OutputFactory()
        output_factory.make_output(
            output_type=self.__get_config_value("output"),  # 输出类型，输出到文件、kafka、终端
            bootstrapservers=self.__get_config_value("bootstrapservers"),
            topic=self.__get_config_value("topic"),
            output_path=self.__get_config_value("outputfile")
        )
        self.outputObj = output_factory.get_output_obj()

    def run(self) -> None:
        self.__make_outputObj()  # 构造输出对象
        delay = self.__get_config_value("delay")
        nums = self.__get_config_value("num")
        data_type = self.__get_config_value("datatype")
        datapatter = self.__get_config_value("datapatter")
        datagenmodule: str = self.__get_config_value("datagenmodule")  # 模块名称
        datagenerator: str = self.__get_config_value("datagenerator")  # 类名称
        dataGenModulePath: str = self.__load_dataGen_module_path(datagenmodule=datagenmodule)  # 模块对应的py文件的绝对路径
        dataGen = self.make_data_generator(datagenerator=datagenerator, dataGenModulePath=dataGenModulePath)
        for value in self.gen_data(dataGen, data_type, nums=nums, patter=datapatter):
            self.outputObj.output_data(value, delay=delay)


if __name__ == '__main__':
    sk_producter = sampleDataProducter(name=__name__, args=sys.argv)
    sk_producter.run()

