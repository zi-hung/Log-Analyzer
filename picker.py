from datetime import datetime, timedelta
from collections.abc import Callable
from parsing import Record



def make_window(end: datetime, hours: int) -> Callable[[Record], bool]: 
    start = end - timedelta(hours=hours)
    def in_window(record: Record) -> bool:
        return start <= record[0] <= end
    return in_window


def filter_records(records: list[Record], keep: Callable[[Record], bool]):
    for record in records:
        if keep(record):
            yield record