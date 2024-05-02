from logging import Filter, LogRecord


class EndpointFilter(Filter):
    def __init__(self, excluded_endpoints: list[str], name: str = "") -> None:
        super().__init__(name)
        self.excluded_endpoints = excluded_endpoints

    def filter(self, record: LogRecord) -> bool:
        return record.args and len(record.args) >= 3 and record.args[2] not in self.excluded_endpoints
