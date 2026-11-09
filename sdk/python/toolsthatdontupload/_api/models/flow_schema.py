from enum import StrEnum


class FlowSchema(StrEnum):
    TTDU_FLOWV1 = "ttdu.flow/v1"

    def __str__(self) -> str:
        return str(self.value)
