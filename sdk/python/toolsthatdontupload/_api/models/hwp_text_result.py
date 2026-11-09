from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.hwp_text_result_format import HwpTextResultFormat
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.hwp_block import HwpBlock
    from ..models.hwp_engine import HwpEngine
    from ..models.hwp_stats import HwpStats


T = TypeVar("T", bound="HwpTextResult")


@_attrs_define
class HwpTextResult:
    """
    Attributes:
        ok (bool):
        text (str):
        blocks (list[HwpBlock]):
        format_ (HwpTextResultFormat | Unset):
        stats (HwpStats | Unset):
        engine (HwpEngine | Unset):
    """

    ok: bool
    text: str
    blocks: list[HwpBlock]
    format_: HwpTextResultFormat | Unset = UNSET
    stats: HwpStats | Unset = UNSET
    engine: HwpEngine | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ok = self.ok

        text = self.text

        blocks = []
        for blocks_item_data in self.blocks:
            blocks_item = blocks_item_data.to_dict()
            blocks.append(blocks_item)

        format_: str | Unset = UNSET
        if not isinstance(self.format_, Unset):
            format_ = self.format_.value

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
                "text": text,
                "blocks": blocks,
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
        from ..models.hwp_block import HwpBlock
        from ..models.hwp_engine import HwpEngine
        from ..models.hwp_stats import HwpStats

        d = dict(src_dict)
        ok = d.pop("ok")

        text = d.pop("text")

        blocks = []
        _blocks = d.pop("blocks")
        for blocks_item_data in _blocks:
            blocks_item = HwpBlock.from_dict(blocks_item_data)

            blocks.append(blocks_item)

        _format_ = d.pop("format", UNSET)
        format_: HwpTextResultFormat | Unset
        if isinstance(_format_, Unset):
            format_ = UNSET
        else:
            format_ = HwpTextResultFormat(_format_)

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

        hwp_text_result = cls(
            ok=ok,
            text=text,
            blocks=blocks,
            format_=format_,
            stats=stats,
            engine=engine,
        )

        hwp_text_result.additional_properties = d
        return hwp_text_result

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
