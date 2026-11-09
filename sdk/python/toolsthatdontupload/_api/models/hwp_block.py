from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Self, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.hwp_block_type import HwpBlockType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.hwp_block_cells_item import HwpBlockCellsItem
    from ..models.hwp_block_nested_in_type_0 import HwpBlockNestedInType0


T = TypeVar("T", bound="HwpBlock")


@_attrs_define
class HwpBlock:
    """
    Attributes:
        type_ (HwpBlockType):
        section (int | Unset):
        text (str | Unset):
        rows (list[list[str]] | Unset):
        cells (list[HwpBlockCellsItem] | Unset):
        nested_in (HwpBlockNestedInType0 | None | Unset):
    """

    type_: HwpBlockType
    section: int | Unset = UNSET
    text: str | Unset = UNSET
    rows: list[list[str]] | Unset = UNSET
    cells: list[HwpBlockCellsItem] | Unset = UNSET
    nested_in: HwpBlockNestedInType0 | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.hwp_block_nested_in_type_0 import HwpBlockNestedInType0

        type_ = self.type_.value

        section = self.section

        text = self.text

        rows: list[list[str]] | Unset = UNSET
        if not isinstance(self.rows, Unset):
            rows = []
            for rows_item_data in self.rows:
                rows_item = rows_item_data

                rows.append(rows_item)

        cells: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.cells, Unset):
            cells = []
            for cells_item_data in self.cells:
                cells_item = cells_item_data.to_dict()
                cells.append(cells_item)

        nested_in: dict[str, Any] | None | Unset
        if isinstance(self.nested_in, Unset):
            nested_in = UNSET
        elif isinstance(self.nested_in, HwpBlockNestedInType0):
            nested_in = self.nested_in.to_dict()
        else:
            nested_in = self.nested_in

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
            }
        )
        if section is not UNSET:
            field_dict["section"] = section
        if text is not UNSET:
            field_dict["text"] = text
        if rows is not UNSET:
            field_dict["rows"] = rows
        if cells is not UNSET:
            field_dict["cells"] = cells
        if nested_in is not UNSET:
            field_dict["nested_in"] = nested_in

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        from ..models.hwp_block_cells_item import HwpBlockCellsItem
        from ..models.hwp_block_nested_in_type_0 import HwpBlockNestedInType0

        d = dict(src_dict)
        type_ = HwpBlockType(d.pop("type"))

        section = d.pop("section", UNSET)

        text = d.pop("text", UNSET)

        _rows = d.pop("rows", UNSET)
        rows: list[list[str]] | Unset = UNSET
        if _rows is not UNSET:
            rows = []
            for rows_item_data in _rows:
                rows_item = cast(list[str], rows_item_data)

                rows.append(rows_item)

        _cells = d.pop("cells", UNSET)
        cells: list[HwpBlockCellsItem] | Unset = UNSET
        if _cells is not UNSET:
            cells = []
            for cells_item_data in _cells:
                cells_item = HwpBlockCellsItem.from_dict(cells_item_data)

                cells.append(cells_item)

        def _parse_nested_in(data: object) -> HwpBlockNestedInType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                nested_in_type_0 = HwpBlockNestedInType0.from_dict(data)

                return nested_in_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(HwpBlockNestedInType0 | None | Unset, data)

        nested_in = _parse_nested_in(d.pop("nested_in", UNSET))

        hwp_block = cls(
            type_=type_,
            section=section,
            text=text,
            rows=rows,
            cells=cells,
            nested_in=nested_in,
        )

        hwp_block.additional_properties = d
        return hwp_block

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
