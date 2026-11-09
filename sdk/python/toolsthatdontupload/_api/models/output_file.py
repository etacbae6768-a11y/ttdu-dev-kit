from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="OutputFile")


@_attrs_define
class OutputFile:
    """
    Attributes:
        name (str):
        mime (str):
        size (int):
        sha256 (str):
        base64 (str):
    """

    name: str
    mime: str
    size: int
    sha256: str
    base64: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        mime = self.mime

        size = self.size

        sha256 = self.sha256

        base64 = self.base64

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "mime": mime,
                "size": size,
                "sha256": sha256,
                "base64": base64,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        name = d.pop("name")

        mime = d.pop("mime")

        size = d.pop("size")

        sha256 = d.pop("sha256")

        base64 = d.pop("base64")

        output_file = cls(
            name=name,
            mime=mime,
            size=size,
            sha256=sha256,
            base64=base64,
        )

        output_file.additional_properties = d
        return output_file

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
