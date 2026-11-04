import re
import logging
from pathlib import Path
from datetime import datetime, timedelta
from collections.abc import Callable
import json

type Record = tuple[datetime, str, str]



class SkipBadLine:
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



def find_log_files(folder: Path) -> list[Path]:
    return sorted(folder.glob("*.log"))


def read_lines(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            yield line.strip("\n")


def parse_line(line: str) -> Record:
    match = re.search(r"(\d+-\d+-\d+\s\d+:\d+:\d+)\s\[([A-Z]+)\]\s(.+)", line)
    if match is None:
        raise ValueError(f"正则匹配失败: {line}")
    time_text, level, msg = match.groups()
    try:
        time = datetime.strptime(time_text, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise ValueError(f"时间不合法: {line}")
    return (time, level, msg)


def make_window(end: datetime, hours: int) -> Callable[[Record], bool]:
    start = end - timedelta(hours=hours)
    def in_window(record: Record) -> bool:
        return start <= record[0] <= end
    return in_window


def filter_records(records: list[Record], keep: Callable[[Record], bool]):
    for record in records:
        if keep(record):
            yield record


def main():
    logging.basicConfig(
    filename="analyzer_run.log",
    encoding="utf-8",
    level=logging.INFO,
    format="%(levelname)s | %(asctime)s | %(message)s"
)

    valid = []
    line_count = 0
    bad_count = 0
    logs = find_log_files(Path("logs"))

    for log in logs:
        logging.info(f"开始扫描: {log.name}")
        skip = SkipBadLine(log)
        for line in read_lines(log):
            line_count += 1
            with skip:
                valid.append(parse_line(line))
        bad_count += skip.bad_count

    fmt = "%Y-%m-%d %H:%M:%S"
    hours = 2
    end = datetime.strptime("2026-11-01 10:00:00", fmt)
    start = end - timedelta(hours=hours)

    keep = make_window(end, hours)
    kept_records = filter_records(valid, keep)

   

    level_count = {}
    kept_records_count = 0
    for record in kept_records:
        kept_records_count += 1
        level_count[record[1]] = level_count.get(record[1], 0) + 1

    

    sorted_level_count = {level: level_count[level] for level in sorted(level_count.keys())}
    
    report = {"window": {"start": start.strftime(fmt),
                       "end": end.strftime(fmt)},
                       "files": [log.name for log in logs],
                       "total_lines": line_count,
                       "bad_lines": bad_count,
                       "in_window": kept_records_count,
                       "level_counts": sorted_level_count}

    with open("report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

        
    print(f"files: {len(logs)}")
    print(f"lines: {line_count} | bad: {bad_count} | in window: {kept_records_count}")
    for level in sorted(level_count.keys()):
        print(f"{level}: {level_count[level]}")
    print("report -> report.json")


    logging.info("报告写入完毕")

main()

    

                