from __future__ import annotations

from collections.abc import Mapping
from io import BytesIO
from typing import Any, Self, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from .. import types
from ..types import UNSET, File, Unset

T = TypeVar("T", bound="FlowRunMultipart")


@_attrs_define
class FlowRunMultipart:
    """
    Attributes:
        flow (str): The flow as a JSON string
        files (list[File]):
        vars_ (str | Unset): Values for the flow's vars, as a JSON object string, e.g. {"client":"ACME"}
    """

    flow: str
    files: list[File]
    vars_: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        flow = self.flow

        files = []
        for files_item_data in self.files:
            files_item = files_item_data.to_tuple()

            files.append(files_item)

        vars_ = self.vars_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "flow": flow,
                "files": files,
            }
        )
        if vars_ is not UNSET:
            field_dict["vars"] = vars_

        return field_dict

    def to_multipart(self) -> types.RequestFiles:
        files: types.RequestFiles = []

        files.append(("flow", (None, str(self.flow).encode(), "text/plain")))

        for files_item_element in self.files:
            files.append(("files", files_item_element.to_tuple()))

        if not isinstance(self.vars_, Unset):
            files.append(("vars", (None, str(self.vars_).encode(), "text/plain")))

        for prop_name, prop in self.additional_properties.items():
            files.append((prop_name, (None, str(prop).encode(), "text/plain")))

        return files

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)
        flow = d.pop("flow")

        files = []
        _files = d.pop("files")
        for files_item_data in _files:
            files_item = File(payload=BytesIO(files_item_data))

            files.append(files_item)

        vars_ = d.pop("vars", UNSET)

        flow_run_multipart = cls(
            flow=flow,
            files=files,
            vars_=vars_,
        )

        flow_run_multipart.additional_properties = d
        return flow_run_multipart

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
