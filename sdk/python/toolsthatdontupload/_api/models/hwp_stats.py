from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="HwpStats")


@_attrs_define
class HwpStats:
    """
    Attributes:
        sections (int | Unset):
        paragraphs (int | Unset):
        tables (int | Unset):
        cells (int | Unset):
        chars (int | Unset):
        pages (int | Unset):
    """

    sections: int | Unset = UNSET
    paragraphs: int | Unset = UNSET
    tables: int | Unset = UNSET
    cells: int | Unset = UNSET
    chars: int | Unset = UNSET
    pages: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        sections = self.sections

        paragraphs = self.paragraphs

        tables = self.tables

        cells = self.cells

        chars = self.chars

        pages = self.pages

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if sections is not UNSET:
            field_dict["sections"] = sections
        if paragraphs is not UNSET:
            field_dict["paragraphs"] = paragraphs
        if tables is not UNSET:
            field_dict["tables"] = tables
        if cells is not UNSET:
            field_dict["cells"] = cells
        if chars is not UNSET:
            field_dict["chars"] = chars
        if pages is not UNSET:
            field_dict["pages"] = pages

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        sections = d.pop("sections", UNSET)

        paragraphs = d.pop("paragraphs", UNSET)

        tables = d.pop("tables", UNSET)

        cells = d.pop("cells", UNSET)

        chars = d.pop("chars", UNSET)

        pages = d.pop("pages", UNSET)

        hwp_stats = cls(
            sections=sections,
            paragraphs=paragraphs,
            tables=tables,
            cells=cells,
            chars=chars,
            pages=pages,
        )

        hwp_stats.additional_properties = d
        return hwp_stats

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
