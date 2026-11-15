# Log Analyzer
扫描 logs/ 下的日志文件，统计指定时间窗内各级别条数，生成 JSON 报告，并把运行过程记录到 analyzer_run.log。

运行：先 `python3 make_logs.py` 生成样例数据，再 `python3 analyzer.py`。开发环境：WSL2 + Ubuntu 26.04 + Python 3.14

「项目结构」:

    reader: 读取日志文件

    parsing: 逐行解析日志文件

    picker: 筛选出符合指定时间窗的记录