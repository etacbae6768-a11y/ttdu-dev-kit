from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.hwp_engine import HwpEngine
    from ..models.hwp_stats import HwpStats
    from ..models.output_file import OutputFile


T = TypeVar("T", bound="HwpDocxResult")


@_attrs_define
class HwpDocxResult:
    """
    Attributes:
        ok (bool):
        outputs (list[OutputFile]):
        format_ (str | Unset):
        stats (HwpStats | Unset):
        engine (HwpEngine | Unset):
    """

    ok: bool
    outputs: list[OutputFile]
    format_: str | Unset = UNSET
    stats: HwpStats | Unset = UNSET
    engine: HwpEngine | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ok = self.ok

        outputs = []
        for outputs_item_data in self.outputs:
            outputs_item = outputs_item_data.to_dict()
            outputs.append(outputs_item)

        format_ = self.format_

        stats: dict[str, Any] | Unset = UNSET
        if not isinstance(self.stats, Unset):
            stats = self.stats.to_dict()

        engine: dict[str, Any] | Unset = UNSET
        if not isinstance(self.engine, Unset):
            engine = self.engine.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ok": ok,
                "outputs": outputs,
            }
        )
        if format_ is not UNSET:
            field_dict["format"] = format_
        if stats is not UNSET:
            field_dict["stats"] = stats
        if engine is not UNSET:
            field_dict["engine"] = engine

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.hwp_engine import HwpEngine
        from ..models.hwp_stats import HwpStats
        from ..models.output_file import OutputFile

        d = dict(src_dict)
        ok = d.pop("ok")

        outputs = []
        _outputs = d.pop("outputs")
        for outputs_item_data in _outputs:
            outputs_item = OutputFile.from_dict(outputs_item_data)

            outputs.append(outputs_item)

        format_ = d.pop("format", UNSET)

        _stats = d.pop("stats", UNSET)
        stats: HwpStats | Unset
        if isinstance(_stats, Unset):
            stats = UNSET
        else:
            stats = HwpStats.from_dict(_stats)

        _engine = d.pop("engine", UNSET)
        engine: HwpEngine | Unset
        if isinstance(_engine, Unset):
            engine = UNSET
        else:
            engine = HwpEngine.from_dict(_engine)

        hwp_docx_result = cls(
            ok=ok,
            outputs=outputs,
            format_=format_,
            stats=stats,
            engine=engine,
        )

        hwp_docx_result.additional_properties = d
        return hwp_docx_result

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
