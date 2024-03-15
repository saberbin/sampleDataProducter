import argparse
from typing import Any, Dict


class ArgsParser(object):
    def __init__(self, description: str) -> None:
        self.parser = argparse.ArgumentParser(description=description)
        # 添加需要解析的参数
        # 配置文件
        self.parser.add_argument("--config", dest="config", type=str, help="config file path default to settings dir file.")
        # 数据配置
        # data_type数据类型，text或者是json；datapatter为分隔符，text数据需要传入，默认为|
        self.parser.add_argument("--datatype", dest="datatype", type=str, default="text", help="output data type, text or json.")
        self.parser.add_argument("--patter", dest="datapatter", type=str, default="|", help="text data split sign, defalut is |.")
        # 生成的数据数量，默认为100条
        self.parser.add_argument("--num", dest="num", default=100, type=int, help="generate data nums, default 100 nums data.")
        # 输出参数，output表示输出到哪里；outputfile表示输出文件路径，
        self.parser.add_argument("--output", dest="output", type=str, default="shell", help="data output way, like kafka or file or shell, default to shell.")
        self.parser.add_argument("--outputfile", dest="outputfile", type=str, default="data", help="text output file only, default data.")
        # kafka相关配置
        self.parser.add_argument("--bootstrapservers", dest="bootstrapservers", type=str, help="kafka bootstrapservers")
        self.parser.add_argument("--topic", dest="topic", type=str, help="kafka topic.")
        # 数据类相关参数
        self.parser.add_argument("--datagenerator", dest="datagenerator", default="WordGenerator", type=str, help="data generator class name")
        self.parser.add_argument("--datagenmodule", dest="datagenmodule", default="null", type=str, help="data generator module path")
        
        self.parser.add_argument("--delay", dest="delay", default=0.1, type=float, help="data output delay")
        # 已解析的参数
        self.parsed_args = None
        # 将所有解析后的参数存放到字典中
        self.arg_items: Dict[str, Any] = dict()
    
    def parse_args(self, args) -> None:
        argsed, _ = self.parser.parse_known_args(args=args)
        self.parsed_args = argsed
        item_list = self.parsed_args._get_kwargs()
        for item in item_list:
            key, value = item
            self.arg_items[key] = value

    def get_value(self, key) -> Any:
        return self.arg_items.get(key, None)

