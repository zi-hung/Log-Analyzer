from datetime import datetime
from pathlib import Path
import logging
import re


type Record = tuple[datetime, str, str]


class SkipBadLine:    # 解析
    def __init__(self, path: Path):
        self.path = path
        self.bad_count = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc_type == ValueError:
            self.bad_count += 1
            logging.warning(f"{self.path.name}: {exc}")
        return exc_type == ValueError



def parse_line(line: str) -> Record: #解析
    match = re.search(r"(\d+-\d+-\d+\s\d+:\d+:\d+)\s\[([A-Z]+)\]\s(.+)", line)
    if match is None:
        raise ValueError(f"正则匹配失败: {line}")
    time_text, level, msg = match.groups()
    try:
        time = datetime.strptime(time_text, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise ValueError(f"时间不合法: {line}")
    return (time, level, msg)