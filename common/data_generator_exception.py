# local Exception


class DataClassNotFoundException(Exception):
    """数据类查找不到异常"""
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


