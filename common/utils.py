from pathlib import Path
from string import ascii_letters, digits
from random import choices


def get_workpath():
    """
    返回当前项目工作目录
    """
    cwd = Path().cwd()
    return cwd


def generate_random_str(length: int=5) -> str:
    values = ascii_letters + digits
    return "".join(choices(values, k=length))


