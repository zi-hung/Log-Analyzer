# Log Analyzer
扫描 logs/ 下的日志文件，统计指定时间窗内各级别条数，生成 JSON 报告，并把运行过程记录到 analyzer_run.log。

运行：先 `python make_logs.py` 生成样例数据，再 `python analyzer.py`。