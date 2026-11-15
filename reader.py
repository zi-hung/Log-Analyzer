from pathlib import Path


def find_log_files(folder: Path) -> list[Path]: #读数据
    return sorted(folder.glob("*.log"))


def read_lines(path: Path): #读
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            yield line.strip("\n")