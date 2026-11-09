from enum import StrEnum


class HwpBlockType(StrEnum):
    PARAGRAPH = "paragraph"
    TABLE = "table"

    def __str__(self) -> str:
        return str(self.value)
