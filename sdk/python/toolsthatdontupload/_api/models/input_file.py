from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="InputFile")


@_attrs_define
class InputFile:
    """
    Attributes:
        name (str):
        base64 (str):
        mime (str | Unset):
    """

    name: str
    base64: str
    mime: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        base64 = self.base64

        mime = self.mime

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "base64": base64,
            }
        )
        if mime is not UNSET:
            field_dict["mime"] = mime

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        name = d.pop("name")

        base64 = d.pop("base64")

        mime = d.pop("mime", UNSET)

        input_file = cls(
            name=name,
            base64=base64,
            mime=mime,
        )

        input_file.additional_properties = d
        return input_file

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
