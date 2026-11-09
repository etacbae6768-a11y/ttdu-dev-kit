from enum import StrEnum


class HwpTextResultFormat(StrEnum):
    HWP = "hwp"
    HWPX = "hwpx"

    def __str__(self) -> str:
        return str(self.value)
