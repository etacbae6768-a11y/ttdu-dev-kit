from enum import StrEnum


class FlowStepScope(StrEnum):
    ALL = "all"
    EACH = "each"

    def __str__(self) -> str:
        return str(self.value)
